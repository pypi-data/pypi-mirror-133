Python library made for drawing neural networks anytime in the script, using pygame.

!!Pygame required to use!!

If you don't have it downloaded already, use: ``pip install pygame``

Download:
``pip install drwnt``

How to use:
This library only has one function, being .draw_net().

To make this whole thing work we need a couple thing to pass in. First we are going to start by writing ``drwnt.draw_net()``
Then we pass in some stuff, being (In this order):

Window we want to draw it on

List of inputs

List of outputs

List of connections between single nodes

List of weights of these connections

List of bias values for each node

Location we want to draw it in (string), either:

"lu" for left up
"ld" for left down
"ru" for right up
"rd" for right down

List of hidden nodes - optional

And now we are done, we let it do it's job and we can just sit back and watch this magic!