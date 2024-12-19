import matplotlib.pyplot as plt
import glob
import os
import numpy as np
import sys
import h5py


def load_scale_bindat(fpath):
    # Load binary data
    with open(fpath, 'rb') as f:
        bin_data = np.fromfile(f, dtype=np.uint16)

    bin_data = bin_data * 0.0001  # reflectance = 1.0e-4 * pixel_value + 0.0
    bin_data = bin_data.reshape(4800, 4800)
    return bin_data


def mask_invalid_values(data, invalid_value=None, range_min=None, range_max=None):
    """
    Mask invalid or out-of-range values in the dataset.
    """
    if invalid_value is not None:
        data = np.ma.masked_equal(data, invalid_value)
    if range_min is not None or range_max is not None:
        data = np.ma.masked_outside(data, range_min, range_max)
    return data


def crop_image(data, imgX=None, imgY=None, crop_size=None):
    """
    Crop the image around the specified center pixel.
    """
    if crop_size is None or imgX is None or imgY is None:
        return data, imgX, imgY  # Return the original data if no cropping is needed

    half_size = crop_size // 2
    x_start = max(imgX - half_size, 0)
    y_start = max(imgY - half_size, 0)
    x_end = min(imgX + half_size + 1, data.shape[1])
    y_end = min(imgY + half_size + 1, data.shape[0])

    cropped_data = data[y_start:y_end, x_start:x_end]
    imgX_relative = imgX - x_start
    imgY_relative = imgY - y_start

    return cropped_data, imgX_relative, imgY_relative


def create_colormap():
    """
    Create a colormap with a special color for masked values.
    """
    cmap = plt.cm.gray
    cmap.set_bad(color='blue')  # Invalid values will be shown in blue
    return cmap


def plot_and_save(data, save_path, cmap, vmin, vmax, imgX_relative=None, imgY_relative=None, label="Reflectance"):
    """
    Plot the data and save it to a file.
    """
    fig, ax = plt.subplots(figsize=(8, 8))
    cax = ax.imshow(data, vmin=vmin, vmax=vmax, cmap=cmap, aspect='auto')
    ax.axis('off')

    # Highlight the center pixel
    if imgX_relative is not None and imgY_relative is not None:
        ax.scatter(imgX_relative, imgY_relative, c='red', s=50, label='Center', zorder=10)

    # Add colorbar
    cbar = fig.colorbar(cax, ax=ax, orientation='vertical', shrink=0.8, pad=0.02)
    cbar.set_label(label)

    # Save the plot
    fig.savefig(save_path, bbox_inches='tight', pad_inches=0)
    plt.close(fig)
    print(f"Image saved to {save_path}")


def plot_image(data, save_path, vmin=0.0, vmax=0.4, invalid_value=None, range_min=None, range_max=None, imgX=None, imgY=None, crop_size=None, label="Reflectance"):
    """
    Main function to process and plot the image.
    """
    # Mask invalid values
    data = mask_invalid_values(data, invalid_value, range_min, range_max)

    # Crop the image
    cropped_data, imgX_relative, imgY_relative = crop_image(data, imgX, imgY, crop_size)

    # Adjust the save path for cropped images
    if crop_size is not None:
        save_path = save_path[:-4] + f"_{crop_size}x{crop_size}.png"

    # Create the colormap
    cmap = create_colormap()

    # Plot and save the image
    plot_and_save(cropped_data, save_path, cmap, vmin, vmax, imgX_relative, imgY_relative, label=label)


def get_save_dir(wd, year, month, day):
    fpath_red = os.path.join(wd, f"data/{year}/{month:02}{day:02}/*VN08.bin")
    fpath_nir = os.path.join(wd, f"data/{year}/{month:02}{day:02}/*VN11.bin")
    ipdat_red = glob.glob(fpath_red)[0]
    ipdat_nir = glob.glob(fpath_nir)[0]

    save_dir = os.path.join(wd, f"output/{year}/{month:02}{day:02}/")
    svdir_red = os.path.join(save_dir, os.path.basename(ipdat_red)[:-3] + "png")
    svdir_nir = os.path.join(save_dir, os.path.basename(ipdat_nir)[:-3] + "png")
    svdir_ndvi = os.path.join(save_dir, os.path.basename(ipdat_nir)[:-8] + "ndvi.png")

    os.makedirs(save_dir, exist_ok = True)

    return ipdat_red, ipdat_nir, svdir_red, svdir_nir, svdir_ndvi


def load_save_binary(ipdir_red, ipdir_nir, svdir_red, svdir_nir, svdir_ndvi, imgX, imgY):
    """
    Load a binary file, process the data, and save it as an image.

    Parameters:
        fpath (str): Path to the binary file to load.
        save_path (str): Path to save the resulting image.
    """
    red = load_scale_bindat(ipdir_red)
    nir = load_scale_bindat(ipdir_nir)
    ndvi = (nir - red) / (nir + red)

    # Plot and save reflectance images
    plot_image(red, svdir_red, vmin=0.0, vmax=0.4, range_min=0.0, range_max=1.0, imgX=imgX, imgY=imgY, label="Reflectance (RED)")
    plot_image(nir, svdir_nir, vmin=0.0, vmax=0.4, range_min=0.0, range_max=1.0, imgX=imgX, imgY=imgY, label="Reflectance (NIR)")
    plot_image(ndvi, svdir_ndvi, vmin=0.0, vmax=1.0, range_min=0.0, range_max=1.0, imgX=imgX, imgY=imgY, label="NDVI")
    plot_image(ndvi, svdir_red, vmin=0.0, vmax=0.4, range_min=0.0, range_max=1.0, imgX=imgX, imgY=imgY, crop_size=301, label="Reflectance (RED)")
    plot_image(ndvi, svdir_nir, vmin=0.0, vmax=0.4, range_min=0.0, range_max=1.0, imgX=imgX, imgY=imgY, crop_size=301, label="Reflectance (NIR)")
    plot_image(ndvi, svdir_ndvi, vmin=0.0, vmax=1.0, range_min=0.0, range_max=1.0, imgX=imgX, imgY=imgY, crop_size=301, label="NDVI")

    return



def extract_and_save_h5_to_bin(h5_file_path, dataset_path, bin_file_path):
    """
    Extract a dataset from an HDF5 file and save it as a binary file in little-endian format.

    Parameters:
        h5_file_path (str): Path to the input HDF5 file.
        dataset_path (str): Path to the dataset inside the HDF5 file (e.g., 'Image_data/Rs_VN11').
        bin_file_path (str): Path to save the binary file.
    """
    # Open the HDF5 file
    with h5py.File(h5_file_path, 'r') as h5_file:
        # Navigate to the dataset
        if dataset_path in h5_file:
            dataset = h5_file[dataset_path][:]
            
            # Convert to little-endian format
            little_endian_data = dataset.astype('<u2')  # '<f4' indicates little-endian float32

            # Save the dataset as a binary file
            little_endian_data.tofile(bin_file_path)
            print(f"Dataset '{dataset_path}' saved to '{bin_file_path}' in little-endian format")
        else:
            print(f"Dataset '{dataset_path}' not found in the HDF5 file")


def create_bin(wd, year, month, day, V, H, h5dir):
    h5_file_path = os.path.join(wd, f"data/{year}/{month:02}{day:02}/GC1SG1_{year}{month:02}{day:02}D01D_T{V:02}{H:02}_L2SG_RSRFQ_3002.h5")  # Replace with your HDF5 file path
    attr_red = "Image_data/Rs_VN08"
    attr_nir = "Image_data/Rs_VN11"
    bin_red_path = f"{h5dir}/GC1SG1_{year}{month:02}{day:02}D01D_T{V:02}{H:02}_L2SG_RSRFQ_3002.Rs_VN08.bin" 
    bin_nir_path = f"{h5dir}/GC1SG1_{year}{month:02}{day:02}D01D_T{V:02}{H:02}_L2SG_RSRFQ_3002.Rs_VN11.bin"
    extract_and_save_h5_to_bin(h5_file_path, attr_red, bin_red_path)
    extract_and_save_h5_to_bin(h5_file_path, attr_nir, bin_nir_path)
    return


def main():
    args = sys.argv
    wd = args[1]
    year = args[2]
    month = args[3]
    day = args[4]
    V = args[5]
    H = args[6]
    imgX = round(float(args[7]))
    imgY = round(float(args[8]))
    h5dir = args[9]

    # create additional data
    create_bin(wd, year, month, day, V, H, h5dir)

    # load and save plot image
    ipdat_red, ipdat_nir, svdir_red, svdir_nir, svdir_ndvi = get_save_dir(wd, year, month, day)
    load_save_binary(ipdat_red, ipdat_nir, svdir_red, svdir_nir, svdir_ndvi, imgX, imgY)



if __name__ == '__main__':
    main()
