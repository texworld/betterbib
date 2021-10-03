Update journal abbreviations.

Instructions:

1. Clone https://github.com/JabRef/abbrv.jabref.org
2. Call `combine_journal_lists.py /tmp/out.csv journals/*`
3. Call `python3 csv-to-json.py /tmp/out.csv journals.json`


### Note

This file is about 8 MiB in size and used to be stored in Git LFS. However, someone kept
cloning the repository several times a day, counting towards my monthly  LFS bandwidth
limit of 1 GiB. This prevented me from using LFS in other projects for half of each
month. See <https://github.com/github/feedback/discussions/5918>.

For now, just take the file out of version control.
