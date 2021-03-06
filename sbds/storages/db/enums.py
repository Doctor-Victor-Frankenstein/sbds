# -*- coding: utf-8 -*-
from sqlalchemy.types import Enum

operation_types_enum = Enum(
    'account_create',
    'account_create_with_delegation',
    'account_update',
    'account_witness_proxy',
    'account_witness_vote',
    'author_reward',
    'cancel_transfer_from_savings',
    'challenge_authority',
    'change_recovery_account',
    'claim_reward_balance',
    'comment',
    'comment_benefactor_reward',
    'comment_options',
    'comment_payout_update',
    'comment_reward',
    'convert',
    'curation_reward',
    'custom',
    'custom_binary',
    'custom_json',
    'decline_voting_rights',
    'delegate_vesting_shares',
    'delete_comment',
    'escrow_approve',
    'escrow_dispute',
    'escrow_release',
    'escrow_transfer',
    'feed_publish',
    'fill_convert_request',
    'fill_order',
    'fill_transfer_from_savings',
    'fill_vesting_withdraw',
    'hardfork',
    'interest',
    'limit_order_cancel',
    'limit_order_create',
    'limit_order_create2',
    'liquidity_reward',
    'pow',
    'pow2',
    'producer_reward',
    'prove_authority',
    'recover_account',
    'report_over_production',
    'request_account_recovery',
    'reset_account',
    'return_vesting_delegation',
    'set_reset_account',
    'set_withdraw_vesting_route',
    'shutdown_witness',
    'transfer',
    'transfer_from_savings',
    'transfer_to_savings',
    'transfer_to_vesting',
    'vote',
    'withdraw_vesting',
    'witness_update',
    name='sbds_operation_types')

