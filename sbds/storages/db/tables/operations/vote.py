# -*- coding: utf-8 -*-

from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import Index
from sqlalchemy import Integer
from sqlalchemy import SmallInteger
from sqlalchemy import Text
from sqlalchemy import UnicodeText
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB

from .. import Base
from ...enums import operation_types_enum
from ...field_handlers import accounts_field


class VoteOperation(Base):
    """

    Steem Blockchain Example
    ======================
    {
      "voter": "steemit78",
      "permlink": "firstpost",
      "author": "steemit",
      "weight": 10000
    }



    """

    __tablename__ = 'sbds_op_votes'
    __table_args__ = (ForeignKeyConstraint(
        ['voter'], ['sbds_meta_accounts.name'],
        deferrable=True,
        initially='DEFERRED',
        use_alter=True),
        ForeignKeyConstraint(
        ['author'], ['sbds_meta_accounts.name'],
        deferrable=True,
        initially='DEFERRED',
        use_alter=True),
        UniqueConstraint('block_num', 'transaction_num',
                         'operation_num', 'raw'),
        Index(
        'ix_sbds_op_votes_accounts',
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

    voter = Column(Text, nullable=True)  # steem_type:account_name_type
    author = Column(Text, nullable=True)  # steem_type:account_name_type
    permlink = Column(UnicodeText, index=True)  # name:permlink
    weight = Column(SmallInteger)  # steem_type:int16_t
    operation_type = Column(operation_types_enum, nullable=False, default='')

    _fields = dict(accounts=lambda x: accounts_field(x, 'vote'), )

    _account_fields = frozenset([
        'voter',
        'author',
    ])
