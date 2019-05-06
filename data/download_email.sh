#!/usr/bin/bash

set -e
mkdir email_data

cd email_data
mkdir download
mkdir spam
mkdir ham
cd download

wget https://spamassassin.apache.org/old/publiccorpus/20050311_spam_2.tar.bz2
bunzip2 20050311_spam_2.tar.bz2
tar -xvf 20050311_spam_2.tar
cd spam_2
for filename in *; do cp "$filename" "../../spam/$filename"_spam2; done;
cd ..

wget https://spamassassin.apache.org/old/publiccorpus/20030228_spam.tar.bz2
bunzip2 20030228_spam.tar.bz2
tar -xvf 20030228_spam.tar
cd spam
for filename in *; do cp "$filename" "../../spam/$filename"_spam; done;
cd ..

wget https://spamassassin.apache.org/old/publiccorpus/20030228_hard_ham.tar.bz2
bunzip2 20030228_hard_ham.tar.bz2
tar -xvf 20030228_hard_ham.tar
cd hard_ham
for filename in *; do cp "$filename" "../../ham/$filename"_hard_ham; done;
cd ..

wget https://spamassassin.apache.org/old/publiccorpus/20030228_easy_ham.tar.bz2
bunzip2 20030228_easy_ham.tar.bz2
tar -xvf 20030228_easy_ham.tar
cd easy_ham
for filename in *; do cp "$filename" "../../ham/$filename"_easy_ham; done;
cd ..

wget https://spamassassin.apache.org/old/publiccorpus/20030228_easy_ham_2.tar.bz2
bunzip2 20030228_easy_ham_2.tar.bz2
tar -xvf 20030228_easy_ham_2.tar
cd easy_ham_2
for filename in *; do cp "$filename" "../../ham/$filename"_easy_ham_2; done;
cd ..

