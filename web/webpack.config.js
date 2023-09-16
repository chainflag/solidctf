const path = require('path');

module.exports = {
    entry: './src/pb.js',
    output: {
        path: path.resolve(__dirname, 'src'),
        filename: 'bundle.js',
        libraryTarget: 'umd',
        library: 'pb',
    }
};
