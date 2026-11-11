export type M1AuthRouteDecision = Readonly<
  | { status: 'selected'; route: 'codex_app_agent'; payer: 'codex_app_account'; connection: 'unverified';selection:'owner_default' }
  | { status: 'selected'; route: 'local_api_byok'; payer: 'user_api_account';connection:'unverified';selection:'explicit_compatibility' }
  | { status: 'blocked'; reason: 'unsupported_route' | 'unsupported_deployment' | 'commercial_review_required'
    | 'inherited_login_not_supported' | 'siwc_outside_m1' }
>;

/** Select the local preview route without inferring account access or release admission. */
export function evaluateM1AuthRoute(route: unknown, deployment: unknown): M1AuthRouteDecision {
  if (route === 'inherited_chatgpt_login') {
    return { status: 'blocked', reason: 'inherited_login_not_supported' };
  }
  if (route === 'sign_in_with_chatgpt') {
    return { status: 'blocked', reason: 'siwc_outside_m1' };
  }
  if (route !== 'local_api_byok' && route !== 'codex_app_agent') {
    return { status: 'blocked', reason: 'unsupported_route' };
  }
  if (deployment === 'commercial_local' || deployment === 'hosted') {
    return { status: 'blocked', reason: 'commercial_review_required' };
  }
  if (deployment !== 'local_engineering_preview') {
    return { status: 'blocked', reason: 'unsupported_deployment' };
  }
  if (route === 'local_api_byok') return {status:'selected',route:'local_api_byok',payer:'user_api_account',connection:'unverified',selection:'explicit_compatibility'};
  // This selects the owner-requested integration route, not an account/worker/cost qualification.
  return { status: 'selected', route: 'codex_app_agent', payer: 'codex_app_account', connection: 'unverified',selection:'owner_default' };
}
