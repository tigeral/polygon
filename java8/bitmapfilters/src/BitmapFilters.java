import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.function.IntConsumer;
import java.util.stream.IntStream;

/**
 * Simple JavaClass to touch with Java 8 features such as Lambdas and CollectionsAPI Streams.
 *
 * Lets open Image file and put its data to int[] where each integer value is a 24bit RGB pixel data.
 * Then wrap this array with a Stream and modify its data with a lambda functions. This function will act like a
 * optical filters in order to apply some visual effect to initial image.
 *
 * Note that the Stream object data couldn't be changes once it was initialized, and even more than that
 * it could be traveled only once. This is done using one of the "termination functions".
 * So, we will wrap the image data with a Stream object, then apply some lambdas to process this data and finally we
 * will collect modified data to the result int[].
 * Complete image data will be stored into result.png file.
 *
 * This program is just a copy of that one which we create during java.io 2.0 RnD Lab contest in Kharkiv on 28.09.2013.
 */
public class BitmapFilters {

    public static void main(String[] args) throws IOException {

        // open image file (file was loaded from the www.stockfreeimages.com web site
        // (http://www.stockfreeimages.com/21049591/Color-Creative-background-07.html)
        File imgPath = new File("./image1.png");
        BufferedImage bufferedImage = ImageIO.read(imgPath);
        // read image data to int[] data buffer
        int[] imgData = new int[bufferedImage.getWidth() * bufferedImage.getHeight()];
        for (int y = 0; y < bufferedImage.getHeight(); y++ ) {
            for (int x = 0; x < bufferedImage.getWidth(); x++ ) {
                int pixelIndex = y * bufferedImage.getWidth() + x;
                imgData[pixelIndex] = bufferedImage.getRGB(x, y);
            }
        }

        // define result data int[] object which would be used from the lambda function.
        int[] resultData = new int[bufferedImage.getWidth() * bufferedImage.getHeight()];
        // define the index to fill resultData object in a strict order. We put index variable into array
        // in order to allow its modification from lambda function,because lambdas couldn't use a non final fields.
        int[] index = {0};

        // define the lambda functions. (uncomment that one which you want to use)
        IntConsumer filter = (pixelData) -> { resultData[index[0]++] = pixelData & 0xff0000;}; // only red chanel
//        IntConsumer filter = (pixelData) -> { resultData[index[0]++] = pixelData & 0x00ff00;}; // only red chanel
//        IntConsumer filter = (pixelData) -> { resultData[index[0]++] = pixelData & 0x0000ff;}; // only red chanel
//        IntConsumer filter = (pixelData) -> { resultData[index[0]++] = pixelData & 0x00ffff;}; // red color excluded

        // wrap image data with a Stream and apply lambda function to it,
        IntStream imgDataStream = Arrays.stream(imgData);
        imgDataStream.forEach(filter);

        // save resultData to file
        bufferedImage.setRGB(0, 0, bufferedImage.getWidth(), bufferedImage.getHeight(), resultData, 0, bufferedImage.getWidth());
        ImageIO.write(bufferedImage, "png", new File("result.png"));
    }
}
