package main

import "fmt"

func main() {
	// nil은 반드시 접근에 실패해서 페이지 폴트가 발생하는 특수한 메모리 접근
	var p *int = nil
	fmt.Println("비정상 메모리 접근 전")
	*p = 0
	fmt.Println("비정상 메모리 접근 후")
}
