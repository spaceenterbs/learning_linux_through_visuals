#!/bin/bash -e

extract() {
    PATTERN=$1
    JSONFILE=$2.json
    OUTFILE=$2.txt

    case $PATTERN in
    read)
        RW=read
        ;;
    randwrite)
        RW=write
        ;;
    *)
        echo "입출력 패턴에 문제가 있습니다: $PATTERN" >&2
        exit 1
    esac

    BW_BPS=$(jq ".jobs[0].${RW}.bw_bytes" $JSONFILE)
    IOPS=$(jq ".jobs[0].${RW}.iops" $JSONFILE)
    LATENCY_NS=$(jq ".jobs[0].${RW}.lat_ns.mean" $JSONFILE)
    echo $BW_BPS $IOPS $LATENCY_NS >$OUTFILE
}

if [ $# -ne 1 ] ; then
    echo "사용법: $0 <설정파일명>" >&2
    exit 1
fi

if [ $(id -u) -ne 0 ] ; then
    echo "프로그램 실행에 루트 권한이 필요합니다" >&2
    exit 1
fi

CONFFILE=$1

. ${CONFFILE}

DATA_FILE=${DATA_DIR}/data
DATA_FILE_SIZE=$((128*1024*1024))
QUEUE_DIR=/sys/block/${DEVICE_NAME}/queue
SCHED_FILE=${QUEUE_DIR}/scheduler
READ_AHEAD_KB_FILE=${QUEUE_DIR}/read_ahead_kb

if [ "$PART_NAME" = "" ] ; then
    DEVICE_FILE=/dev/${DEVICE_NAME}
else
    DEVICE_FILE=/dev/${PART_NAME}
fi

if [ ! -e ${DATA_DIR} ] ; then
    echo "존재하지 않는 데이터 디렉터리 (${DATA_DIR})입니다" >&2
    exit 1
fi

if [ ! -e ${DEVICE_FILE} ] ; then
    echo "존재하지 않는 디바이스 파일 (${DEVICE_FILE})입니다" >&2
    exit 1
fi

mount | grep -q ${DEVICE_FILE}
RET=$?
if [ ${RET} != 0 ] ; then
    echo "마운트되지 않은 디바이스 파일 (${DEVICE_FILE})입니다" >&2
    exit 1
fi

if [ ! -e ${SCHED_FILE} ] ; then
     echo "존재하지 않는 입출력 스케줄러 파일 (${SCHED_FILE})입니다" >&2
     exit 1
fi

SCHEDULERS="mq-deadline none"

if [ ! -e ${READ_AHEAD_KB_FILE} ] ; then
    echo "존재하지 않는 미리 읽기 설정 파일 (${READ_AHEAD_KB_FILE})입니다" >&2
    exit 1
fi

mkdir -p ${TYPE}
rm -f ${DATA_FILE}
dd if=/dev/zero of=${DATA_FILE} oflag=direct,sync bs=${DATA_FILE_SIZE} count=1

COMMON_FIO_OPTIONS="--name linux-in-practice --group_reporting --output-format=json --filename=${DATA_FILE} --filesize=${DATA_FILE_SIZE}"

# 미리 읽기 효과 확인용 데이터 수집

## 데이터 수집

SIZE=${DATA_FILE_SIZE}
BLOCK_SIZE=$((1024*1024))

for SCHED in ${SCHEDULERS} ; do
    echo ${SCHED} >${SCHED_FILE}
    for READ_AHEAD_KB in 128 0 ; do
        echo ${READ_AHEAD_KB} >${READ_AHEAD_KB_FILE}
        echo "pattern: read, sched: ${SCHED}, read_ahead_kb: ${READ_AHEAD_KB}" >&2
        FIO_OPTIONS="${COMMON_FIO_OPTIONS} --readwrite=read --size=${SIZE} --bs=${BLOCK_SIZE}"
        FILENAME_PATTERN="${TYPE}/read-${SCHED}-${READ_AHEAD_KB}"
        echo 3 >/proc/sys/vm/drop_caches
        fio ${FIO_OPTIONS} >${FILENAME_PATTERN}.json
        extract read ${FILENAME_PATTERN}
    done
done

## 데이터 가공

OUTFILENAME=${TYPE}/read.txt
rm -f ${OUTFILENAME}

for SCHED in ${SCHEDULERS} ; do
    for READ_AHEAD_KB in 128 0 ; do
        FILENAME=${TYPE}/read-${SCHED}-${READ_AHEAD_KB}.txt
        awk -v sched=${SCHED} -v read_ahead_kb=${READ_AHEAD_KB} '{print sched, read_ahead_kb, $1}' <$FILENAME >>${OUTFILENAME}
    done
done

# 입출력 스케줄러 효과 확인용 데이터 수집

## 데이터 수집

SIZE=$((4*1024*1024))
BLOCK_SIZE=$((4*1024))
JOB_PATTERNS=$(seq $(grep -c processor /proc/cpuinfo))

for SCHED in ${SCHEDULERS} ; do
    echo ${SCHED} >${SCHED_FILE}
    for NUM_JOBS in ${JOB_PATTERNS}; do
        echo "pattern: randwrite, sched: ${SCHED}, numjobs: ${NUM_JOBS}" >&2
        FIO_OPTIONS="${COMMON_FIO_OPTIONS} --direct=1 --readwrite=randwrite --size=${SIZE} --bs=${BLOCK_SIZE} --numjobs=${NUM_JOBS}"
        FILENAME_PATTERN="${TYPE}/randwrite-${SCHED}-${NUM_JOBS}"
        echo 3 >/proc/sys/vm/drop_caches
        fio ${FIO_OPTIONS} >${FILENAME_PATTERN}.json
        extract randwrite ${FILENAME_PATTERN}
    done
done

## 데이터 가공

for SCHED in ${SCHEDULERS} ; do
    OUTFILENAME=${TYPE}/randwrite-${SCHED}.txt
    rm -f ${OUTFILENAME}
    for NUM_JOBS in ${JOB_PATTERNS} ; do
        FILENAME=${TYPE}/randwrite-${SCHED}-${NUM_JOBS}.txt
        awk -v num_jobs=${NUM_JOBS} '{print num_jobs, $2, $3}' <$FILENAME >>${OUTFILENAME}
    done
done

./plot-block.py

rm ${DATA_FILE}
