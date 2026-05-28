# DEPLOYMENT DOMAIN

**Status:** Reserved for future frontend testing.
**Frontend status:** Not active.
**Deployment status:** Not active.
**DNS delegation status:** Active in Cloudflare.
**Temporary domain:** `epistemiclab.dpdns.org`

This document records the temporary domain plan for the project without starting
frontend implementation or production deployment.

## Purpose

The temporary domain is reserved only for future learner-facing frontend tests.
It must not be treated as a production release, Examiner deployment, or evidence
that backend governance gates have been cleared.

## Current Repository State

- The repository has no active frontend application.
- The repository has no active web deployment pipeline.
- The intended temporary custom domain is `epistemiclab.dpdns.org`.
- The domain is delegated from DigitalPlat to Cloudflare nameservers.
- No custom domain is currently bound to an active GitHub Pages deployment.
- DNS records are managed in Cloudflare and documented here for traceability.
- DNS provider API keys must not be committed to the repository.

## Intended GitHub Pages Setup

When the frontend phase begins, the expected temporary setup is:

1. Build the frontend into a static output directory.
2. Publish that static output through GitHub Pages.
3. Add a `CNAME` file to the published Pages source containing the custom
   domain on a single line.
4. Delegate the DigitalPlat domain to an external DNS provider if needed.
5. Configure DNS records at the delegated DNS provider.
6. Enable HTTPS after GitHub Pages verifies the domain.

## DigitalPlat API Scope

DigitalPlat's API base URL is:

```text
https://domain-api.digitalplat.org/api/v1
```

The API authenticates with:

```text
Authorization: Bearer <api-key>
```

API keys must be treated as secrets and must not be committed to this
repository.

The documented DigitalPlat API supports:

- Listing domains owned by the authenticated key.
- Registering a domain with external nameservers.
- Updating the delegated nameserver set for a domain.
- Deleting a domain.

The documented API does not expose DNS record management endpoints for records
such as `A`, `AAAA`, `CNAME`, or `TXT`. That means the GitHub Pages DNS record
must be created at whichever external DNS provider receives the delegated
nameservers.

For example, if `epistemiclab.dpdns.org` is delegated to Cloudflare, the
`CNAME` record must be created in Cloudflare, not in this repository and not
through the currently documented DigitalPlat domain API.

## Required DNS Record

At the delegated DNS provider, create:

```text
Type:  CNAME
Name:  epistemiclab
Value: BuenasBox.github.io
TTL:   Auto or 300
Proxy: DNS only, if using Cloudflare
```

Some DNS providers may require the full hostname as the record name:

```text
epistemiclab.dpdns.org CNAME BuenasBox.github.io
```

Then the published GitHub Pages source must include a `CNAME` file containing:

```text
epistemiclab.dpdns.org
```

## Cloudflare Setup Without Touching Other Production Sites

Use a separate Cloudflare zone for `epistemiclab.dpdns.org`. Do not edit the DNS
zone for any existing production site.

1. In Cloudflare, select **Add a domain**.
2. Enter:

   ```text
   epistemiclab.dpdns.org
   ```

3. Choose the free plan unless a paid feature is explicitly needed.
4. Skip importing records if Cloudflare does not discover any existing records.
5. Copy the two Cloudflare nameservers assigned to this new zone:

   ```text
   maria.ns.cloudflare.com
   olof.ns.cloudflare.com
   ```
6. In DigitalPlat, update only `epistemiclab.dpdns.org` to use those two
   Cloudflare nameservers.
7. Return to Cloudflare and wait for the zone to become active.
8. In the new `epistemiclab.dpdns.org` zone, add the GitHub Pages DNS record:

   ```text
   Type:  CNAME
   Name:  @
   Value: BuenasBox.github.io
   TTL:   Auto
   Proxy: DNS only
   ```

   If Cloudflare rejects `@` for this delegated subdomain zone, use the full
   hostname:

   ```text
   Type:  CNAME
   Name:  epistemiclab.dpdns.org
   Value: BuenasBox.github.io
   TTL:   Auto
   Proxy: DNS only
   ```

9. Do not enable redirects, page rules, workers, WAF rules, or origin settings
   for this new zone during initial setup.
10. After the future frontend is published, add `epistemiclab.dpdns.org` as the
    custom domain in GitHub Pages and enable HTTPS.

Safety checks before changing DigitalPlat nameservers:

- Confirm the Cloudflare dashboard is showing the zone
  `epistemiclab.dpdns.org`, not another production domain.
- Confirm the DigitalPlat PATCH URL contains
  `epistemiclab.dpdns.org/nameservers`.
- Confirm the JSON body contains only the two Cloudflare nameservers assigned
  to this new zone.
- Do not use the nameservers from an unrelated existing Cloudflare zone unless
  Cloudflare explicitly assigned the same pair to `epistemiclab.dpdns.org`.

Assigned Cloudflare nameservers for `epistemiclab.dpdns.org`:

```text
maria.ns.cloudflare.com
olof.ns.cloudflare.com
```

DigitalPlat API verification returned `success: true`, and public DNS
resolution confirmed these nameservers for `epistemiclab.dpdns.org`.

Cloudflare CNAME flattening is active at the zone apex. Public `A` resolution
for `epistemiclab.dpdns.org` returns the GitHub Pages address set:

```text
185.199.108.153
185.199.109.153
185.199.110.153
185.199.111.153
```

Public `AAAA` resolution also returns the GitHub Pages IPv6 address set. A
direct public `CNAME` query may return the zone SOA instead of a CNAME because
Cloudflare flattens apex CNAME records.

## Optional DigitalPlat API Checks

To inspect the domain without exposing the API key in shell history, set it as
an environment variable first:

```powershell
$env:DIGITALPLAT_API_KEY = "<api-key>"
Invoke-RestMethod `
  -Uri "https://domain-api.digitalplat.org/api/v1/domains" `
  -Headers @{ Authorization = "Bearer $env:DIGITALPLAT_API_KEY" }
```

If the domain is registered but delegated to the wrong DNS provider, update its
nameservers with:

```powershell
$body = @{
  nameservers = @(
    "ns1.provider.example",
    "ns2.provider.example"
  )
} | ConvertTo-Json

Invoke-RestMethod `
  -Method Patch `
  -Uri "https://domain-api.digitalplat.org/api/v1/domains/epistemiclab.dpdns.org/nameservers" `
  -Headers @{
    Authorization = "Bearer $env:DIGITALPLAT_API_KEY"
    "Content-Type" = "application/json"
  } `
  -Body $body
```

Only run the nameserver update after confirming the external DNS provider's
actual assigned nameservers.

For this temporary domain, the DNS record should normally be:

```text
epistemiclab.dpdns.org CNAME BuenasBox.github.io
```

For a project Pages site under the `BuenasBox` organization, custom subdomains
normally use a DNS `CNAME` record pointing to:

```text
BuenasBox.github.io
```

For an apex/root domain, GitHub Pages requires DNS records at the provider
instead of a repository-only change. Confirm the current GitHub Pages
documentation before activation because DNS and HTTPS behavior can change over
time.

## Activation Checklist

Before activating the domain:

- Confirm the exact temporary domain name: `epistemiclab.dpdns.org`.
- Confirm the DNS provider where the domain is managed.
- Decide whether the test URL will use the apex domain, `www`, or a subdomain
  such as `app`.
- Decide the deployment platform: GitHub Pages, Vercel, Netlify, or another
  host.
- Add the required `CNAME` file only to the actual published static source.
- Verify DNS resolution from a terminal before sharing the URL.
- Keep the domain labeled as temporary/testing in release notes and project
  documentation.

## Non-Goals

- No frontend implementation is started by this decision.
- No backend API is exposed by this decision.
- No Examiner scoring surface is enabled by this decision.
- No production claims are made by this decision.
