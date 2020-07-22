package main

import (
	"log"
	"time"
	"net/http"
)

var cliEnvironment string
var cliConfigPath string

type httpResponse struct {
	url      string
	response *http.Response
	err      error
}

type gamesettings struct {
	RequestsPerCycle int
	CycleSleep       int
	Url              string
}

// TODO: Add arguments for RPC, CS, and Url defaults
func retrieveGenSettings() gamesettings {

	defaultSettings := gamesettings{RequestsPerCycle: 5, CycleSleep: 5, Url: "http://localhost:8080/timestamp"}

	log.Printf("gamesettings: %v\n", defaultSettings)

	return defaultSettings
}

func requestsGenerator() {

	gameSettings := retrieveGenSettings()

	for {
		log.Println("starting batch requests...")
		responses := asyncHttpRequests(gameSettings.Url, gameSettings.RequestsPerCycle)
		log.Println("completed batch requests")
		log.Println(responses)

		time.Sleep(time.Second * time.Duration(gameSettings.CycleSleep))
	}
}

func asyncHttpRequests(url string, requestsPerCycle int) []*httpResponse {

	ch := make(chan *httpResponse)
	responses := []*httpResponse{}
	client := http.Client{}
	log.Printf("executing %d requests", requestsPerCycle)
	for r := 0; r < requestsPerCycle; r++ {
		go func(url string) {
			// log.Printf("Fetching %s \n", url)
			resp, err := client.Get(url)
			ch <- &httpResponse{url, resp, err}
			if err != nil && resp != nil && resp.StatusCode == http.StatusOK {
				resp.Body.Close()
			}

			log.Printf("Response: %s \n",)
		}(url)
	}

	// for {
	// 	select {
	// 	case r := <-ch:
	// 		log.Printf("%s was fetched\n", r.url)
	// 		if r.err != nil {
	// 			log.Println("with an error", r.err)
	// 			responses = append(responses, r)
	// 		} else {
	// 			responses = append(responses, r)
	// 			for _, response := range responses {
	// 				log.Printf("response: %v", response)
	// 			}
	// 			return responses
	// 		}
	// 	case <-time.After(50 * time.Millisecond):
	// 		log.Printf(".")
	// 	}
	// }
	return responses
}

func main() {

	requestsGenerator()
}
