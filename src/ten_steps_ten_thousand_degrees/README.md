# Summary

I found a very interesting game called [ten steps ten thousand degrees](https://www.taptap.com/app/35537) last year.

It's easy to play, but it's very brain consuming.

# How to play

You can download to your Android phone, and install it.

After you start the game, there will be a stack of clocks arranged regularly, all of which have only one pointer. 

1. Click on a clock and the pointer on it will turn clockwise by 90 degrees. 

2. If there is another clock at the angle at which the hands stop, then this clock will also rotate 90 degrees. 

3. Repeat 2 until there is no clock in the direction the pointer is pointing.

You only have ten chances to click. The system will count the rotation angles of all the clocks after each click. If the score required by the current level is reached, it is judged as a victory.

# What I do here

I wrote a small script that can play this game in a random walk based on the defined initial state of the game.

The code is also very simple, the core walking logic is in the class called GameStatus. It is about 21 lines.

The game simulation logic is in the function action_at, only passing the status, and the position you want to click. 

It will return the score the action does, and the final status it will be.

Class StatusManager is helping to do the cache. It is quite simple, can help to avoid some of unnecessary recomputing.

The main function have some settings to start the simulation, and output the result.