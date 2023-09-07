/*

cache

1. 2^2(=4)K바이트부터 2^2.25K바이트, 2^2.5K바이트, ...식으로 최종적으로 64M바이트가 될 때까지 다음 처리를 반복

   1) 숫자에 해당하는 크기의 버퍼를 확보
   2) 버퍼의 모든 캐시라인에 순차적으로 접근. 마지막 캐시라인까지 접근했으면 다시 첫 캐시라인으로 돌아가고, 최종적으로 소스 코드에 지정한 NACCESS번 메모리에 접근함
   3) 접근 1회당 걸린 시간을 기록

2. 1에서 나온 결과를 바탕으로 그래프를 작성해서 cache.jpg 파일로 저장

*/

package main

import (
	"fmt"
	"log"
	"math"
	"os"
	"os/exec"
	"syscall"
	"time"
)

const (
	CACHE_LINE_SIZE = 64
	// 프로그램이 제대로 동작하지 않으면 이 값을 변경
	// 성능이 좋은 PC라면 접근 횟수가 부족해서 버퍼 크기가 작은 경우의 결과 값이 이상할 수 있으므로 큰 값을 사용
	// 느린 PC라면 시간이 오래 걸릴 수 있으므로 작은 값을 사용
	NACCESS = 128 * 1024 * 1024
)

func main() {
	_ = os.Remove("out.txt")
	f, err := os.OpenFile("out.txt", os.O_CREATE|os.O_RDWR, 0660)
	if err != nil {
		log.Fatal("openfile()에 실패했습니다")
	}
	defer f.Close()
	for i := 2.0; i <= 16.0; i += 0.25 {
		bufSize := int(math.Pow(2, i)) * 1024
		data, err := syscall.Mmap(-1, 0, bufSize, syscall.PROT_READ|syscall.PROT_WRITE, syscall.MAP_ANON|syscall.MAP_PRIVATE)
		defer syscall.Munmap(data)
		if err != nil {
			log.Fatal("mmap()에 실패했습니다")
		}

		fmt.Printf("버퍼 크기 2^%.2f(%d) KB 데이터 수집중...\n", i, bufSize/1024)
		start := time.Now()
		for i := 0; i < NACCESS/(bufSize/CACHE_LINE_SIZE); i++ {
			for j := 0; j < bufSize; j += CACHE_LINE_SIZE {
				data[j] = 0
			}
		}
		end := time.Since(start)
		f.Write([]byte(fmt.Sprintf("%f\t%f\n", i, float64(NACCESS)/float64(end.Nanoseconds()))))
	}
	command := exec.Command("./plot-cache.py")
	out, err := command.Output()
	if err != nil {
		fmt.Fprintf(os.Stderr, "명령어 실행에 실패했습니다: %q: %q", err, string(out))
		os.Exit(1)
	}
}
