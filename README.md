# rsync_backup
A simple rsync based backup tool with a configurable fail-safe to stop it mass deleting files if excess source files have mistakenly been deleted.

I personally wanted this just for my photos where once a week I rsync from one computer to a NAS. I didn't want some complicated backup software to track all the versions of files each week, just a straight clone was sufficient. 
However I was always concerned that if I accidentally deleted a source directory and didn't notice then it would purge it from my NAS too, hence defeating the point of having a backup. So I wrote this script to check how many files rsync was going to delete first before doing anything. If its over a limit I've set, then don't do anything and I'll investigate first.

It has a number of simple features:
1. A configurable deletion limit, e.g. if it detects that more than 50 files are going to be deleted, it stops and does nothing, instead sending you an email
2. All configuration elements are driven from a yaml config file
3. It has simple logging, so you can keep track of what the tool has done in the past
4. You can configure multiple source/destination pairs to rync/backup

Setup your config file, test it, then deploy it via cron and hopefully forget about until you mistakenly delete a directory and it sends you an email.

It requires Python 3.5.x and you'll most likely have to install the Python YAML libraries.

If you use gmail... 
Be aware that gmail has a configuration item that prevents less secure clients from sending emails to it. You have to allow access via the the following page:
https://www.google.com/settings/security/lesssecureapps

Also worth considering creating a second email account for this instead of using your main one. I'm not a big fan of adding passwords to config files, but haven't found a better/simple alternative. So hence using a separate email account for the time being. If this email account is compromised then I really don't care...

Let me know what you think/how it can be improved.