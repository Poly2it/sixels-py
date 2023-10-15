import timeit

from PIL import Image

from sixels import encode_image

def main():
    image_path = "test1.png"
    image = Image.open(image_path)
    image = image.resize((128, 128), Image.Resampling.NEAREST) # Image.Resampling.LANCZOS

    execution_time = timeit.timeit(lambda: encode_image(image), number=5) / 5
    encoded_string = encode_image(image)

    print(f"{min(len(image.getcolors()), 256)} colors, {image.width}*{image.height}: {round(execution_time, 4)}s")
    print(encoded_string)

    image_path = "test2.png"
    image = Image.open(image_path)
    image = image.resize((128, 128), Image.Resampling.NEAREST) # Image.Resampling.LANCZOS

    execution_time = timeit.timeit(lambda: encode_image(image), number=5) / 5
    encoded_string = encode_image(image)

    print(f"{min(len(image.getcolors()), 256)} colors, {image.width}*{image.height}: {round(execution_time, 4)}s")
    print(encoded_string)

if __name__ == "__main__":
    main()
