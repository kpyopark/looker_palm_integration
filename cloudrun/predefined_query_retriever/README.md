## Retriever for predefined SQLs.

사전에, 이미 Vector Database에 Predefined SQL이 적재되어 있고 이를 사용자 Question에 맞추어 필터를 추출하고, 사용자에게 결과값을 제시해 주는 서비스이다. 

사용하기 전에 아래 .env 파일을 생성할 것. 아니면 추가적으로 외부 env를 이용하여 Setting할 것.

export LOCATION=<<vector table이 존재하는 리젼>>
export TARGET_LOCATION=<<업무 테이블이 존재하는 리젼>>
export DATASET=<<vector table이 존재하는 리젼>>
export TABLE_NAME=<<vector table명>>
export PROJECT_ID=<<project id>>
