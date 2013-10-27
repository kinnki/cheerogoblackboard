import java.io.IOException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class BlackBoard {

	public static void main(String[] args) throws IOException {
		Document doc = Jsoup.connect(
				"http://www.cheerego.com/dome_web/guest.php").get();
		Elements blackBoardElements = doc.select("#blackboardID div");
		String blackBoardHtml = blackBoardElements.html();
		String regex = "http://\\S*\\.jpg";
		Pattern pattern = Pattern.compile(regex);
		Matcher matcher = pattern.matcher(blackBoardHtml);
		String imageUrls = new String();
		while (matcher.find()) {
			imageUrls += (matcher.group() + "\r\n");
		}
		System.out.println(imageUrls);
		Element contentElement = blackBoardElements.last();
		String contentHtml = contentElement.html();
		contentHtml = contentHtml.replaceAll("<br\\s*/>", "");
		String text = imageUrls + blackBoardHtml;
		System.out.println(text);
	}
}
