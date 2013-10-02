import javax.imageio.ImageIO;
import java.awt.image.BufferedImage;
import java.io.File;
import java.io.IOException;
import java.util.Arrays;
import java.util.function.IntUnaryOperator;
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
 */
public class BitmapFilters {

    public static void main(String[] args) throws IOException {
        // open image file (file was loaded from the www.stockfreeimages.com web site
        // (http://www.stockfreeimages.com/21049591/Color-Creative-background-07.html)
        File imgPath = new File("./image1.png");
        BufferedImage bufferedImage = ImageIO.read(imgPath);
        int[] imgData = bufferedImage.getRGB(0, 0, bufferedImage.getWidth(), bufferedImage.getHeight(), null, 0, bufferedImage.getWidth());

        // define the lambda function to apply some visual effects to image
        IntUnaryOperator resultFunction = Filters.EXCEPT_RED.andThen(Filters.SEPIA.andThen(Filters.TO_GRAYSCALE));
        // wrap image data with a Stream and apply lambda function to it,
        IntStream imgDataStream = Arrays.stream(imgData);
        int[] resultData = imgDataStream.map(resultFunction).toArray();
        // save resultData to file
        bufferedImage.setRGB(0, 0, bufferedImage.getWidth(), bufferedImage.getHeight(), resultData, 0, bufferedImage.getWidth());
        ImageIO.write(bufferedImage, "png", new File("result.png"));
    }

    /**
     * Define different visual effects as an enum in a lambda function notation.
     * So this class both implements enum and IntUnaryOperator interface.
     */
    private enum Filters implements IntUnaryOperator {
        ONLY_RED((pixelData) -> {return  pixelData & 0xff0000;}),
        ONLY_GREEN((pixelData) -> {return  pixelData & 0x00ff00;}),
        ONLY_BLUE((pixelData) -> {return  pixelData & 0x0000ff;}),
        EXCEPT_RED((pixelData) -> {return  pixelData & 0x00ffff;}),
        EXCEPT_GREEN((pixelData) -> {return  pixelData & 0xff00ff;}),
        EXCEPT_BLUE((pixelData) -> {return  pixelData & 0xffff00;}),
        TO_GRAYSCALE((pixelData) -> {
            int red = (pixelData & 0xff0000) >> 16;
            int green = (pixelData & 0x00ff00) >> 8;
            int blue = pixelData & 0x0000ff;
            int average = (red + green + blue) / 3;
            return (average << 16) + (average << 8) + average;
        }),
        SEPIA((pixelData) -> {
            int red = (pixelData & 0xff0000) >> 16;
            int green = (pixelData & 0x00ff00) >> 8;
            int blue = pixelData & 0x0000ff;
            int resultRed = (int)Math.min((red * .393) + (green *.769) + (blue * .189), 255);
            int resultGreen = (int)Math.min((red * .349) + (green *.686) + (blue * .168), 255);
            int resultBlue = (int)Math.min((red * .272) + (green *.534) + (blue * .131), 255);
            return (resultRed << 16) + (resultGreen << 8) + resultBlue;
        });

        private final IntUnaryOperator lambdaFunction;

        // enum classes requires constructor to initialise an inner value (in our case it's a lambdaFunction field).
        private Filters(IntUnaryOperator lambda) {
            this.lambdaFunction = lambda;
        }

        // implement functional method of IntUnaryOperator interface.
        @Override
        public int applyAsInt(int operand) {
            return lambdaFunction.applyAsInt(operand);
        }
    }
}
