
class Actor():
    '''Interface to be implemented by each game character
    '''
    def move(self):
        '''Called by Arena, at the actor's turn
        '''
        raise NotImplementedError('Abstract method')

    def collide(self, other: 'Actor'):
        '''Called by Arena, whenever the `self` actor collides with some
        `other` actor
        '''
        raise NotImplementedError('Abstract method')

    def position(self) -> (int, int, int, int):
        '''Return the rectangle containing the actor, as a 4-tuple of ints:
        (left, top, width, height)
        '''
        raise NotImplementedError('Abstract method')

    def symbol(self) -> (int, int, int, int):
        '''Return the position (x, y, w, h) of current sprite, if it is contained in
        a larger image, with other sprites. Otherwise, simply return (0, 0, 0, 0)
        '''
        raise NotImplementedError('Abstract method')

