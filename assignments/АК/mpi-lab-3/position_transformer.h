//
// Created by maksim on 17.10.20.
//

#ifndef MPI_LAB_3_CLION_POSITION_TRANSFORMER_H
#define MPI_LAB_3_CLION_POSITION_TRANSFORMER_H

struct PositionTransformer {
private:
    double yh;
    double xh;

    int block_pos_x;
    int block_pos_y;

    int block_size_x;
    int block_size_y;
public:

    PositionTransformer(double yh, double xh, int block_pos_y, int block_pos_x, int blockSizeY, int blockSizeX)
            : yh(yh), xh(xh), block_pos_x(block_pos_x), block_pos_y(block_pos_y), block_size_x(blockSizeX),
              block_size_y(blockSizeY) {}

    double y(int cell_y) const {
        return (block_pos_y * block_size_y + cell_y) * yh;
    }

    double x(int cell_x) const {
        return (block_pos_x * block_size_x + cell_x) * xh;
    }
};

#endif //MPI_LAB_3_CLION_POSITION_TRANSFORMER_H
