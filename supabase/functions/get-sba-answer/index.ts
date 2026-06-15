/**
 * Edge Function: get-sba-answer
 *
 * Returns feedback AFTER user submits answer.
 * Only called after answer is submitted.
 *
 * Returns:
 *   - correctness: is_correct, correct_index, correct_letter
 *   - explanation: main text + causal chain
 *   - feedback_by_mode: mentor, trainer, reviewer
 *   - governance: safe_for_examiner, disclaimer
 *   - watermark: user_id, issued_at, expires_at
 *
 * Does NOT expose:
 *   - Mark scheme internals
 *   - Evaluator reasoning
 *   - Official WSET authority claims
 */

import { createClient } from '@supabase/supabase-js';

// =============================================================================
// TYPES
// =============================================================================

interface SBAFeedback {
  id: string;
  correctness: {
    is_correct: boolean;
    correct_index: number;
    correct_letter: string;
  };
  explanation?: {
    main: string;
    causal_chain?: any;
  };
  feedback_by_mode?: {
    mentor?: string;
    trainer?: string;
    reviewer?: string;
  };
  governance?: {
    safe_for_examiner: boolean;
    disclaimer: string;
  };
  _watermark: {
    user_id: string;
    issued_at: string;
    expires_at: string;
  };
}

interface AnswerSubmission {
  item_id: string;
  user_answer: number; // 0-3 (option index)
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

function error(message: string, status = 400, code?: string) {
  return new Response(JSON.stringify({ error: message, code }), {
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
  userId: string
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
  // Only POST allowed
  if (req.method !== 'POST') {
    return error('Method not allowed', 405);
  }

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
    // 3. PARSE REQUEST BODY
    // =====================================================================

    let submission: AnswerSubmission;

    try {
      const body = await req.json();
      submission = body as AnswerSubmission;
    } catch (err) {
      return error('Invalid JSON in request body', 400);
    }

    // Validate submission
    if (!submission.item_id) {
      return error('Missing item_id', 400);
    }

    if (typeof submission.user_answer !== 'number' || submission.user_answer < 0 || submission.user_answer > 3) {
      return error('Invalid user_answer (must be 0-3)', 400);
    }

    // =====================================================================
    // 4. FETCH ITEM FROM DATABASE
    // =====================================================================

    const { data: item, error: fetchError } = await supabase
      .from('sba_items')
      .select('*')
      .eq('id', submission.item_id)
      .single();

    if (fetchError || !item) {
      return error('Item not found', 404);
    }

    // =====================================================================
    // 5. BUILD FEEDBACK RESPONSE
    // =====================================================================

    const isCorrect = submission.user_answer === item.correct_index;

    const watermark = {
      user_id: user_id,
      issued_at: new Date().toISOString(),
      expires_at: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
    };

    const feedback: SBAFeedback = {
      id: item.id,
      correctness: {
        is_correct: isCorrect,
        correct_index: item.correct_index,
        correct_letter: item.correct_letter
      },
      explanation: item.feedback_by_mode ? {
        main: '',
        causal_chain: item.causal_chain
      } : undefined,
      feedback_by_mode: item.feedback_by_mode,
      governance: item.governance || {
        safe_for_examiner: false,
        disclaimer: 'PROTOTIPO · ENTRENAMIENTO · NO EVALUACIÓN OFICIAL WSET'
      },
      _watermark: watermark
    };

    // =====================================================================
    // 6. RETURN FEEDBACK
    // =====================================================================

    return success(feedback);

  } catch (err) {
    console.error('Unexpected error:', err);
    return error('Internal server error', 500);
  }
}

// For Deno Deploy
Deno.serve(handler);
