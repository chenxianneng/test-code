package main

import (
	"fmt"
	"io"
	"net/http"
)

type Msg struct {
	SendFrom string
	data     string
}

type msgList []Msg

var msgQueue map[string]msgList

func main() {
	msgQueue = make(map[string]msgList)

	http.HandleFunc("/send", sendHandle)
	http.HandleFunc("/recv", recvHandle)
	e := http.ListenAndServe(":8888", nil)
	if e != nil {
		fmt.Println(e.Error())
	}
}

func sendHandle(w http.ResponseWriter, r *http.Request) {

	if r.Method == http.MethodGet {
		if err := r.ParseForm(); err != nil {
			fmt.Fprintf(w, "ParseForm() err: %v", err)
			return
		}

		sendFrom := r.FormValue("sendfrom")
		sendTo := r.FormValue("sendto")
		data := r.FormValue("data")

		var msgInfo Msg
		msgInfo.SendFrom = sendFrom
		msgInfo.data = data

		_, ok := msgQueue[sendTo]
		if ok == true {
			if len(msgQueue[sendTo]) >= 200 {
				msgQueue[sendTo] = msgQueue[sendTo][1:]
			}

			// for i := 0; i < len(msgQueue[sendTo]); i++ {
			// }

			msgQueue[sendTo] = append(msgQueue[sendTo], msgInfo)
		} else {
			var temp msgList
			msgQueue[sendTo] = temp
			msgQueue[sendTo] = append(msgQueue[sendTo], msgInfo)
		}

		result := "ok"
		_, e := io.WriteString(w, result)
		if e != nil {
			fmt.Println(e.Error())
		} else {
			fmt.Println("ok")
		}
	}
}

func recvHandle(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodGet {
		if err := r.ParseForm(); err != nil {
			fmt.Fprintf(w, "ParseForm() err: %v", err)
			return
		}

		myDeviceID := r.FormValue("myid")
		result := ""
		_, ok := msgQueue[myDeviceID]
		if ok == true {
			for i := 0; i < len(msgQueue[myDeviceID]); i++ {
				result = result + msgQueue[myDeviceID][i].data + "send from:" + msgQueue[myDeviceID][i].SendFrom + "\n"
			}
			var temp msgList
			msgQueue[myDeviceID] = temp
		} else {
			result = "none"
		}

		_, e := io.WriteString(w, result)
		if e != nil {
			fmt.Println(e.Error())
		} else {
			fmt.Println("ok")
		}
	}
}
