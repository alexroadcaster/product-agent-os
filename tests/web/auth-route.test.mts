import assert from 'node:assert/strict';
import { test } from 'node:test';
import { evaluateM1AuthRoute } from '../../packages/contracts/auth/m1-route.ts';

test('local M1 selects only the user-paid API route and leaves account verification pending', () => {
  assert.deepEqual(evaluateM1AuthRoute('local_api_byok', 'local_engineering_preview'), {
    status: 'selected', route: 'local_api_byok', payer: 'user_api_account', connection: 'unverified',
  });
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
