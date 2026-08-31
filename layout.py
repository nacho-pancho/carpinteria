from util import *
from geometry import *
from core import *
"""
Various layouts besides the default
"""


#--------------------------------------------------------------------

class StackLayout(Layout): 
    """ 
    splits a volume into a vertical pile of slices along the Z axis
    """

    def __init__(self,num_slots:int,axis:int):
        super().__init__('stack')
        self.num_slots = num_slots
        self.axis = axis
        if axis != X_COORD and axis != Y_COORD and axis != Z_COORD:
            raise ValueError(f'Invalid axis {axis}.')

    def slots(self):
        return self.num_slots

    def __str__(self):
        return f'StackLayout along axis {self.axis} with {self.num_slots} slots.'
    
    def apply(self, _volume:Volume, _parts:tuple[PieceSpec]):
        #
        # parts are arranged in increasing value along the axis
        # the assignment is greedy and respects the weights
        # if the sum of weights ls larger than 1, a warning is produced
        # and the result will be inconsistent

        logger = get_logger()
        logger.info(f'Applying layout {self} to volume {_volume} with {self.num_slots} slots.')
        # the initial available size is the whole volume
        # and its offset is the same as the base volume
        unallocated_volume = copy.deepcopy(_volume)
        for i,part in enumerate(_parts):
            if part is None:
                logger.info(f'Part {i} is empty.')
                continue
            # the alignment along the layout axis must be fixed to 'Left/Top/Right'
            piece = part.piece
            cons  = part.constraints
            orig_cons  = copy.deepcopy(cons)
            cons.alignment[self.axis] = LEFT # same as TOP and FRONT
            simple_layout(unallocated_volume,part)
            #
            # once laid out we tweak two things:
            # 1) the actual slot volume is reduced retroactively according to the piece volume
            #
            part.slot_volume = copy.deepcopy(unallocated_volume)
            margin_size = cons.margin.size()
            padding_size = cons.padding.size()
            # piece takes up all available space along axis, so piece volume and available are the same here
            # infer padded size from piece volume along axis
            part.available_volume.size.dim[self.axis] = part.piece_volume.size.dim[self.axis] 
            logger.info(f'Available volume (inferred back) {part.available_volume}')

            part.padded_volume.size.dim[self.axis] = part.available_volume.size.dim[self.axis] + margin_size.dim[self.axis]
            # infer slot size along axis from padded
            logger.info(f'Padded volume (inferred back) {part.padded_volume}')

            part.slot_volume.size.dim[self.axis] = \
                part.padded_volume.size.dim[self.axis] - padding_size.dim[self.axis]
            logger.info(f'Slot volume (inferred back) {part.slot_volume}')
            
            #
            # 2) we remove the slot volume from the beginning of the unallocated volume
            #    and move offset accordingly
            unallocated_volume.size.dim[self.axis]      -= part.slot_volume.size.dim[self.axis]
            unallocated_volume.offset.coords[self.axis] += part.slot_volume.size.dim[self.axis]

            #
            # if the part is a composite, lay it out
            #
            if isinstance(part.piece,CompositePiece):
                part.piece.apply_layout()


    
    def to_dict(self):
        d = super().to_dict()
        d['axis'] = self.axis
        return d

    
    def from_dict(d:dict):
        return StackLayout(d['slots'],d['axis'])

LAYOUTS={'default':DefaultLayout,
         'stack':StackLayout
         }