/**
 * Edge Function: get-sba-questions
 *
 * Returns SBA question list (before user submits answer).
 * Does NOT expose:
 *   - correct_index
 *   - correct_answer
 *   - feedback
 *   - causal_chain internals
 *   - misconception model
 *
 * DOES expose:
 *   - id
 *   - text (question)
 *   - options (4 answer choices)
 *   - topic
 *   - ra (responsibility area)
 *   - difficulty
 *
 * Enforces:
 *   - Authentication (user must be logged in)
 *   - Plan validation (demo/premium/full_access)
 *   - Trial expiration (for demo users)
 *   - RLS (backend filtering by user plan)
 */

import { createClient } from '@supabase/supabase-js';

// =============================================================================
// TYPES
// =============================================================================

interface SBAQuestion {
  id: string;
  text: string;
  options: string[];
  topic?: string;
  ra?: string;
  difficulty?: string;
  _watermark?: {
    user_id: string;
    issued_at: string;
    expires_at: string;
  };
}

interface SBAQuestionsResponse {
  items: SBAQuestion[];
  count: number;
  offset: number;
  limit: number;
  total?: number;
}

interface ErrorResponse {
  error: string;
  code?: string;
  details?: string;
}

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function success<T>(data: T, status = 200) {
  return new Response(JSON.stringify(data), {
    headers: { 'Content-Type': 'application/json' },
    status
  });
}

function error(message: string, status = 400, code?: string, details?: string) {
  const response: ErrorResponse = { error: message, code, details };
  return new Response(JSON.stringify(response), {
    headers: { 'Content-Type': 'application/json' },
    status
  });
}

function parseAuthHeader(authHeader: string | null): string | null {
  if (!authHeader) return null;
  if (authHeader.startsWith('Bearer ')) {
    return authHeader.substring(7);
  }
  return null;
}

// =============================================================================
// VALIDATION
// =============================================================================

async function validateAuthToken(req: Request, supabase: any): Promise<{ user_id: string } | null> {
  const authHeader = req.headers.get('authorization');
  const token = parseAuthHeader(authHeader);

  if (!token) {
    return null;
  }

  try {
    const { data: { user }, error } = await supabase.auth.getUser(token);
    if (error || !user) {
      return null;
    }
    return { user_id: user.id };
  } catch (err) {
    console.error('Auth validation error:', err);
    return null;
  }
}

async function validatePlan(
  supabase: any,
  userId: string,
  requiredPlan: string = 'demo'
): Promise<{ allowed: boolean; plan: string | null }> {
  try {
    const { data: profile, error } = await supabase
      .from('user_profiles')
      .select('plan, trial_expires_at')
      .eq('user_id', userId)
      .single();

    if (error || !profile) {
      return { allowed: false, plan: null };
    }

    const { plan, trial_expires_at } = profile;

    // Check trial expiration for demo users
    if (plan === 'demo' && trial_expires_at) {
      const now = new Date();
      const expiresAt = new Date(trial_expires_at);
      if (now > expiresAt) {
        return { allowed: false, plan };
      }
    }

    // Allow premium, full_access, and admin users
    if (['premium', 'full_access', 'admin', 'test'].includes(plan)) {
      return { allowed: true, plan };
    }

    // Allow demo if not expired
    if (plan === 'demo') {
      return { allowed: true, plan };
    }

    return { allowed: false, plan };
  } catch (err) {
    console.error('Plan validation error:', err);
    return { allowed: false, plan: null };
  }
}

// =============================================================================
// MAIN HANDLER
// =============================================================================

export async function handler(req: Request): Promise<Response> {
  // Initialize Supabase client
  const supabaseUrl = Deno.env.get('SUPABASE_URL');
  const supabaseKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');

  if (!supabaseUrl || !supabaseKey) {
    console.error('Missing Supabase environment variables');
    return error('Server configuration error', 500);
  }

  const supabase = createClient(supabaseUrl, supabaseKey);

  try {
    // =====================================================================
    // 1. AUTHENTICATION
    // =====================================================================

    const authResult = await validateAuthToken(req, supabase);
    if (!authResult) {
      return error('Unauthorized', 401);
    }

    const { user_id } = authResult;

    // =====================================================================
    // 2. PLAN VALIDATION
    // =====================================================================

    const planResult = await validatePlan(supabase, user_id);
    if (!planResult.allowed) {
      return error('Plan does not include SBA access', 403);
    }

    // =====================================================================
    // 3. PARSE REQUEST PARAMETERS
    // =====================================================================

    const url = new URL(req.url);
    const limit = Math.min(parseInt(url.searchParams.get('limit') || '25'), 100);
    const offset = Math.max(parseInt(url.searchParams.get('offset') || '0'), 0);
    const topic = url.searchParams.get('topic') || null;

    // Validate parameters
    if (limit < 1 || limit > 100) {
      return error('Invalid limit (1-100)', 400);
    }

    if (offset < 0) {
      return error('Invalid offset (must be >= 0)', 400);
    }

    // =====================================================================
    // 4. QUERY DATABASE (with RLS)
    // =====================================================================

    // Build query
    let query = supabase
      .from('sba_items')
      .select('id, text, options, topic, ra, difficulty', { count: 'exact' });

    if (topic) {
      query = query.eq('topic', topic);
    }

    query = query
      .order('id')
      .range(offset, offset + limit - 1);

    const { data: items, count, error: dbError } = await query;

    if (dbError) {
      console.error('Database error:', dbError);
      return error('Failed to fetch questions', 500);
    }

    // =====================================================================
    // 5. ADD WATERMARK TO ALL ITEMS
    // =====================================================================

    const watermark = {
      user_id: user_id,
      issued_at: new Date().toISOString(),
      expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString() // 24 hours
    };

    const watermarkedItems = (items || []).map((item: any) => ({
      ...item,
      _watermark: watermark
    }));

    // =====================================================================
    // 6. RETURN RESPONSE
    // =====================================================================

    const response: SBAQuestionsResponse = {
      items: watermarkedItems,
      count: watermarkedItems.length,
      offset: offset,
      limit: limit,
      total: count
    };

    return success(response);

  } catch (err) {
    console.error('Unexpected error:', err);
    return error('Internal server error', 500);
  }
}

// For Deno Deploy
Deno.serve(handler);
