# -*- coding: utf-8 -*-
#

from .dedup_doi import main as dedup_doi
from .format import main as format
from .journal_abbrev import main as journal_abbrev
from .sync import main as sync

__all__ = ["dedup_doi", "format", "journal_abbrev", "sync"]
