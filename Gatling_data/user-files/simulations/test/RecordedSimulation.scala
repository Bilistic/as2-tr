package test

import scala.concurrent.duration._

import io.gatling.core.Predef._
import io.gatling.http.Predef._
import io.gatling.jdbc.Predef._

class RecordedSimulation extends Simulation {

	val httpProtocol = http
		.baseURL("http://35.232.60.112:5000")
		.inferHtmlResources()
		.acceptHeader("image/webp,image/apng,image/*,*/*;q=0.8")
		.acceptEncodingHeader("gzip, deflate")
		.acceptLanguageHeader("en-GB,en-US;q=0.9,en;q=0.8")
		.userAgentHeader("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36")

	val headers_0 = Map(
		"Accept" -> "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
		"Upgrade-Insecure-Requests" -> "1")

	val headers_1 = Map("Pragma" -> "no-cache")

    val uri1 = "https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"
    val uri2 = "https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0"
    val uri3 = "https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js"

	val scn = scenario("RecordedSimulation")
		.exec(http("request_0")
			.get("/index/")
			.headers(headers_0))
		.pause(1)
		.exec(http("request_1")
			.get("/favicon.ico")
			.headers(headers_1))
		.pause(101)
		// GetPage
		// GetIcon
		// GetIconv2

	setUp(scn.inject(atOnceUsers(10))).protocols(httpProtocol)
}