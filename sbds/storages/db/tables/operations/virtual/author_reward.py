# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import SmallInteger
from sqlalchemy import Text
from sqlalchemy import UnicodeText
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from ... import Base
from ....enums import asset_types_enum
from ....enums import operation_types_enum
from ....field_handlers import accounts_field
from ....field_handlers import amount_field
from ....field_handlers import amount_symbol_field


class AuthorRewardVirtualOperation(Base):
    """

    Steem Blockchain Example
    ======================




    """

    __tablename__ = 'sbds_op_virtual_author_rewards'
    __table_args__ = (ForeignKeyConstraint(
        ['author'], ['sbds_meta_accounts.name'],
        deferrable=True,
        initially='DEFERRED',
        use_alter=True),
        UniqueConstraint('block_num', 'transaction_num',
                         'operation_num', 'raw'),
        Index(
        'ix_sbds_op_virtual_author_rewards_accounts',
        'accounts',
        postgresql_using='gin',
        postgresql_ops={'accounts': 'jsonb_path_ops'}))

    _id = Column(BigInteger, autoincrement=True, primary_key=True)
    block_num = Column(Integer, nullable=False)
    transaction_num = Column(SmallInteger, nullable=False)
    operation_num = Column(SmallInteger, nullable=False)
    timestamp = Column(DateTime(timezone=False))
    trx_id = Column(Text, nullable=False)
    accounts = Column(JSONB)
    raw = Column(JSONB)

    author = Column(Text, nullable=True)  # steem_type:account_name_type
    permlink = Column(UnicodeText, index=True)  # name:permlink
    sbd_payout = Column(Numeric(20, 6), nullable=False)  # steem_type:asset
    sbd_payout_symbol = Column(
        asset_types_enum, nullable=False)  # steem_type:asset
    steem_payout = Column(Numeric(20, 6), nullable=False)  # steem_type:asset
    steem_payout_symbol = Column(
        asset_types_enum, nullable=False)  # steem_type:asset
    vesting_payout = Column(Numeric(20, 6), nullable=False)  # steem_type:asset
    vesting_payout_symbol = Column(
        asset_types_enum, nullable=False)  # steem_type:asset
    operation_type = Column(operation_types_enum, nullable=False, default='')

    _fields = dict(
        sbd_payout=lambda x: amount_field(x.get('sbd_payout'), num_func=float),  # steem_type:asset
        sbd_payout_symbol=lambda x: amount_symbol_field(x.get('sbd_payout')),  # steem_type:asset
        steem_payout=lambda x: amount_field(
            x.get('steem_payout'), num_func=float),  # steem_type:asset
        steem_payout_symbol=lambda x: amount_symbol_field(
            x.get('steem_payout')),  # steem_type:asset
        vesting_payout=lambda x: amount_field(
            x.get('vesting_payout'), num_func=float),  # steem_type:asset
        vesting_payout_symbol=lambda x: amount_symbol_field(
            x.get('vesting_payout')),  # steem_type:asset
        accounts=lambda x: accounts_field(x, 'author_reward'),
    )

    _account_fields = frozenset([
        'author',
    ])
