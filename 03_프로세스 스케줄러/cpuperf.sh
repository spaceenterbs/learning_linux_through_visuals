#!/bin/bash

usage() {
    exec >&2
    echo "사용법: $0 [-m] <최대 프로세스 개수>
    1. 'cpuperf.data' 파일에 성능 정보를 저장합니다.
        * 엔트리 개수는 <최대 프로세스 개수>
        * 출력 형식은 '<프로세스 개수> <평균 턴어라운드 타임[초]> <스루풋[프로세스/초]>'
    2. 성능 정보를 바탕으로 평균 턴어라운드 타임 그래프를 만들어서 'avg-tat.jpg'에 저장합니다.
    3. 같은 방법으로 스루풋 그래프를 만들어서 'throughput.jpg'에 저장합니다.

    -m 옵션은 multiload.sh 프로그램에 그대로 전달합니다."
    exit 1
}

measure() {
    local nproc=$1
    local opt=$2
    bash -c "time ./multiload.sh $opt $nproc" 2>&1 | grep real | sed -n -e 's/^.*0m\([.0-9]*\)s$/\1/p' | awk -v nproc=$nproc '
BEGIN{
    sum_tat=0
}
(NR<=nproc){
    sum_tat+=$1
}
(NR==nproc+1) {
    total_real=$1
}
END{
    printf("%d\t%.3f\t%.3f\n", nproc, sum_tat/nproc, nproc/total_real)
}'
}

while getopts "m" OPT ; do
    case $OPT in
        m)
            MEASURE_OPT="-m"
            ;;
        \?)
            usage
            ;;
    esac
done

shift $((OPTIND - 1))

if [ $# -lt 1 ]; then
    usage
fi

rm -f cpuperf.data
MAX_NPROC=$1
for ((i=1;i<=MAX_NPROC;i++)) ; do
    measure $i $MEASURE_OPT  >>cpuperf.data
done

./plot-perf.py $MAX_NPROC
