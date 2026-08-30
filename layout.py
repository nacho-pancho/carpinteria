from util import *
from geometry import *
from core import *

#--------------------------------------------------------------------

def simple_layout(_volume:Volume, part:Part):
    logger = get_logger()
    logger.info(f'Layoing out part {part.piece} within  {_volume} with coinstraints {part.constraints}')

    piece = part.piece
    cons  = part.constraints
    #
    # there are three volumes:
    # the slot volume; that is the total size inside the volume in this case
    # the padded volume, which results from the base volume being grown by the padding
    # the available volume, which results from the padded volume being reduced by the margins
    #
    # we keep track of them all
    part.base_volume = copy.deepcopy(_volume)
    logger.info(f'Base volume {part.base_volume}')
    part.slot_volume = copy.deepcopy(part.base_volume)
    # apply weights
    for i in range(3):
        part.slot_volume.size.dim[i] *= cons.weight[i]

    logger.info(f'Slot volume {part.slot_volume} after applying weight')
    part.padded_volume = grow_volume(part.slot_volume,cons.padding)
    logger.info(f'Padded volume {part.padded_volume}')
    part.available_volume = shrink_volume(part.padded_volume,cons.margin)
    logger.info(f'Available volume {part.available_volume}')
    #
    # we must reserve space for the margin, but this includes padding
    #
    margin_size = cons.margin.size()
    reserved_size = shrink_size(margin_size,cons.padding)
    # now we have the available volume
    # we take into account the piece's own constraints (min and max size)
    # to determine its final size
    # the margin is rigid so it needs to be taken into account in min_size

    piece_size = Size()
    for i in range(3):
        _min = piece.min_size.dim[i]
        _max = piece.max_size.dim[i]
        _ava = part.available_volume.size.dim[i]
        if _min  > _ava:
            logger.warning(f'Available space {_ava} not enough for min size {_min}!')
        piece_size.dim[i] = max(_min, min(_ava,_max))

    part.piece.volume = Volume(piece_size,copy.deepcopy(part.available_volume.offset))

    logger.info(f'Piece volume {part.piece.volume} (prior to alignment)')
    for i in range(3):
        delta = (part.available_volume.size.dim[i] - part.piece.volume.size.dim[i])
        logger.info(f'Excess volume at dimension {i} is {delta}')
        if cons.alignment[i] == CENTER:
            logger.info(f'Center alignment implies displacement by {delta/2}.')
            part.piece.volume.offset.coords[i] += delta / 2
        elif cons.alignment[i] == RIGHT or cons.alignment == BACK or cons.alignment == TOP:
            logger.info(f'right/top/back alignment implies displacement by {delta}.')
            part.piece.volume.offset.coords[i] += delta
    #
    # the final part is the placement of the piece if the piece
    # is smaller than the effective volume, it needs to be arranged
    # according to the alignment
    # 
    # put the piece according to the constraints
    part.piece_volume = part.piece.volume
    logger.info(f'Final volume {piece.volume} (after alignment)')


#--------------------------------------------------------------------

class DefaultLayout(Layout):
    """
    puts one thing inside
    """
    def __init__(self):
        super().__init__('default')

    def apply(self, _volume:Volume, _parts:tuple[Part]):

        logger = get_logger()
        logger.info(f'Applying layout {self} to volume {_volume}')
        # determine size of object
        if _parts[0] is None:
            logger.info(f'No parts to lay out.')
            return
        simple_layout(_volume,_parts[0])

    
    def slots(self):
        return 1

    def __str__(self):
        return self.type()



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
    
    def apply(self, _volume:Volume, _parts:tuple[Part]):
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