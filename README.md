# DQ-AI



This "AI" results of jealousis.
Some of my friends were playing a mobile game nammed "Duel Quiz" which is a game based on questions on overall knowledge.

After a while, I start playing with them. But I was loosing...
I conclude these defeats were because the game was bad designed... And not for any other reasons!

But I could find a way to be sure to win and it's where this program come.

First I look for an API. But it's a little game so it doesn't have one...
Things get harder...

So here is how I build this program :
The idea is simple, I want to create a file with all the questions (DataBase.txt) and their corresponding right answer. If in a game, I have a question I have already met, I can answer correctly thanks to this file. If not, I save it and I will correctly answer the next time.

The main challenge here is to allow the program to interact with the game while there is no API. So I download an emulator (Nox) for Android on my laptop. Then, I need an OCR (Optical Character Recognition) to capture questions and answers. I found one on GitHub which is nammed pytesser and work perfectly in python. And as you can see it represent the main part of my program. The only script I wrote is DuelQuizAI.py.

And we are done!

It is properly working. But I underestimate one factor...
The time needed to save all the questions is HUGE!

Duel Quiz has about 30,000 different questions.
I figure out that to save all these questions, I will need something around 30 nights of 8 hours, in theory...

I stil trained it for some couple hours (that's why the DataBase.txt file has saved about 350 questions) but I encounter some issue that I was not expecting. Let me explain quickly how I was training my algorithm. 

I need to do lot of matches to save all the questions. Unfortunately, Duel Quiz does not have a solo mode or something like that... But there is a way to face random player. So I use this mode to train the algorithm. The plan was to find a random player, play against it for one round, save the answer and then surrender, and face an other random player. So I won't have to wait the other player to play its round which would make me lost some time.

This plan seems to be fine on the paper but some player were challenging me back, sending a friend request or sending a message saying that playing and then surrender was stupid as f***. Abviously, my algorithm was not prepared for this xD so he couldn't do its job properly. Thus even if I let it run for a night, he could have bug after ten minutes and only save a couple questions while I could have expected a thousand more.

Plus, this probleme is both hard to fix and will significantly reduce the pace of the training. So I don't implement it.
So I give up this idea.

I could also, rather than save all the answers, look for the right answer on the internet. This seems to be a good idea, but I couldn't have found time to implement it yet.

So, to conlude, this program is finished... All the functions are done and work perfectly fine, but you need to let it run to save all the questions and its right answer. I won't  do it.

But any way, if you want to try it, contact me (guillaume1.thomas@protonmail.com), and I will explain you the set up you need to make it work

Thanks for your attention
