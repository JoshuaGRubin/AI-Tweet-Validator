#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple batch script that when invoked populates our data directory with
some interesting characters.

June, 2019
@author: Joshua Rubin
"""

import downloadTweetsByUser as dt

maxTweets = 1000

dataDir   = '../../data/raw'

# Choose a diverse bunch who tweet.
people = [ '@BernieSanders',    # Bernie Sanders
           '@elonmusk',         # Elon Musk
           '@ewarren',          # Elizabeth Warren
           '@drfeifei',         # Fei-Fei Li
           '@HamillHimself',    # Mark Hamill
           '@Oprah',            # Oprah Winfrey
           '@realDonaldTrump',  # Donald Trump
           '@scotusginsburg',   # Rith Bader Ginsburg
           '@Slavojiek',        # Slavoj Žižek
           '@StephenCurry30',   # Stephen Curry
           '@tim_cook',         # Tim Cook
           '@YoYo_Ma'         ] # Yo-Yo Ma

for person in people:
    print('Retrieving: ' + person)
    dt.getTweetsByUser(person, outputPath = dataDir, maxTweets = maxTweets)