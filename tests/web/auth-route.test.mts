import assert from 'node:assert/strict';
import { test } from 'node:test';
import { evaluateM1AuthRoute } from '../../packages/contracts/auth/m1-route.ts';

test('owner-selected local M1 uses Codex App agents without an API key or inferred host access', () => {
  assert.deepEqual(evaluateM1AuthRoute('codex_app_agent', 'local_engineering_preview'), {
    status: 'selected', route: 'codex_app_agent', payer: 'codex_app_account', connection: 'unverified',selection:'owner_default',
  });
  assert.deepEqual(evaluateM1AuthRoute('local_api_byok', 'local_engineering_preview'), {status:'selected',route:'local_api_byok',payer:'user_api_account',connection:'unverified',selection:'explicit_compatibility'});
  assert.deepEqual(evaluateM1AuthRoute('inherited_chatgpt_login', 'local_engineering_preview'), {
    status: 'blocked', reason: 'inherited_login_not_supported',
  });
  assert.deepEqual(evaluateM1AuthRoute('sign_in_with_chatgpt', 'local_engineering_preview'), {
    status: 'blocked', reason: 'siwc_outside_m1',
  });
});

test('BYOK selection leaves paid and hosted use behind the commercial gate', () => {
  for (const deployment of ['commercial_local', 'hosted']) {
    assert.deepEqual(evaluateM1AuthRoute('local_api_byok', deployment), {
      status: 'blocked', reason: 'commercial_review_required',
    });
  }
  assert.deepEqual(evaluateM1AuthRoute('local_api_byok', null), {
    status: 'blocked', reason: 'unsupported_deployment',
  });
});
