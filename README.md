# Python으로 구현하는 영화 추천 웹 서비스
- CI/CD
  - 백엔드 CI 자동화 : AWS EC2의 Gitlab-runner
    - 프론트엔드 배포 : Github Pages, Cloudflare
- 파일 구조
  - data 폴더 : 영화 정보에 대한 데이터 셋 csv 파일이 들어있다.
  - model 폴더의 finalized_model.sav 파일 : [recommender.py](http://recommender.py)에서 pickle.dump로 생성된 유저들의 rating 정보를 행렬로 정리된 파일
  - movie_preprocessor.py : 데이터 전처리 로직 파일이다.
  - [recommender.py](http://recommender.py) : 영화 추천 알고리즘
  - [resolver.py](http://resolver.py) : 랜덤으로 영화 반환 혹은 랜덤으로 같은 장르의 영화를 반환해주는 파일이다.
  - venv : 파이썬 가상환경 폴더다.
# 트러블 슈팅

- 백엔드 코드의 지속적인 통합을 위한 gitlab과 vscode 연결이 되지 않아서 약 2시간 넘게 트러블 슈팅한 결과, vscode로 확장 프로그램 gitlab을 설치해서 연동하면 commit과 push가 커멘드 팔레트에서 정상적으로 작동되지 않았다. 그 이유는 왼쪽 source control(버전 관리)에서 message를 입력하지 않았기 때문이다. 그래서 나는 gitlab 사이트에서 code 버튼을 누르고 https로 ide 열기로 연동을 하고 source control로 commit, push를 하기로 했다.
- gitignore에서 가상환경 폴더를 푸시하기 위해선 .gitignore 파일에서 venv를 모두 지워야 푸시된다. 그 이유는 가상환경 파일을 자동으로 무시하게끔 세팅되어 있기 때문이다.
    
    
- 1개의 영화에 평점 5점을 주고 결과를 볼려고 했는데 다음과 같은 오류가 난다. error message를 확인해 보니 ValueError: axis 1 index 1938 exceeds matrix dimension 610 오류가 난다. 해석하면 “값 오류: 축 1 인덱스 1938이 행렬 차원 610을 초과합니다.” 라고 나온다. 내부 코드상에 문제인 것 처럼 보이는데 잘 모르겠다. → 알고보니 데이터 행렬 즉, 배열의 길이가 설정된 크기(610) 만큼 같아야하는데 2571로 초과해서 그렇다.  데이터 셋 csv 파일 작은거 말고 용량 큰걸로 다운 받아야 해결 될 것으로 보인다. → 그렇게 생각해서 하루 종일 데이터 셋을 다운 받았지만 작동이 잘 되지 않았다. 계속해서 이것저것 시도해보니, rating.csv와 movie.csv의 데이터 셋 인덱스가 맞지 않아서 그랬다. 그래서 인덱스를 맞추어 주었더니 작동이 잘 됐다.
    
    
- gitlab-runner(자동 배포 장치)로 배포를 끝내고 잘 배포 되었는지 ec2 인스턴스로 생성하고 연결한 ip주소로 검색해서 들어가봤는데 안 들어가져서 확인해보니 gitlab-runner에서 gitlab-ci.yml에서 설정한 태그 이름과 실제 gitlab에서 등록된 태그 이름이 매치가 잘 못 되어서 배포가 제대로 되지 않았다.
- aws를 통해 ec2에서 생성된 ip주소의 도메인 이름을 구입하고 추가로 aws certificate manager로 https 보안 연결을 할 수 있다.
- CORS(Cross-Origin-Resource-Sharing)의 약자로 프론트엔드가 다른 “origin”(프로토콜 http, https, 도메인 이름, 포트 번호등을 의미)에 있는 백엔드와 통신하는 상황을 의미한다. → 내가 사용하는 FastAPI에서는 CORSMiddleware를 사용해서 origin을 안전하게 연결시켜준다.
- snippet(스니펫)이란 재사용 가능한 조각 코드 즉, 환경 설정을 위한 임포트등을 뜻한다.
- 위에서 작성한 asix 에러를 해결하기 위해서 좀 더 큰 행렬차원의 파일을 다운 받으려고 했지만 api키로 작업하는 일이다 보니 최소 20시간 이상 걸리며 네트워크가 중간에 끊겨질경우 설치가 취소되며, 또 같은 요청을 몇번 반복하면 api 서버에서 로봇인 줄 알고 차단한다고 한다. 이 문제 또한 해결하기 위해서 로봇이 아님을 증명하기 위한 User-Agent 값을 헤더에 넣어줘서 요청을 보냈지만 5시간 설치하다가 또 차단당했다. 그래서 결국 위에서 제시한 해결 방법대로 데이터 셋 파일의 인덱스를 맞추어 주었더니 해결이 되었다.

  # 공부한 내용

- Python으로 구현하는 영화 추천 웹 서비스
    - 공부한 내용
        - Fast API와 Implicit 라이브러리란? Fast API는 파이썬 웹 프레임워크이고 Implicit은 머신러닝을 구축(추천 머신러닝 구축)하는데 필요한 행렬 학습 라이브러리다.
        - 토큰이란? 클라이언트의 정보를 보관하는 보안적인 방법이다.
        - 영화 추천을 하기 위해선 데이터셋(무비렌즈 등등)이 필요하고 추가로 pandas(데이터 분석 및 조작 패키지 column추가 등등), requests(WEB http요청을 다루기위한 패키지) 패키지를 설치해야한다.
        - implict 패키지의 ALS(alternating least squares)함수의 변수들의 역할
            - latent factor란 머신러닝 학습에서 사용자의 요구 데이터(기준)이 실제 데이터와 얼마나 적합한지를 나타낸다.
            - regularization이란 latent factor가 높으면 과적합(학습한 데이터만 정확도가 높음)이 일어날 수 있는데 이를 방지한다.
            - dtype은 data type의 약자다.
            - iterations는 parameter(latent factor, regularization, dtype 등)의 업데이트를 몇번할 지 정하는 변수다.
        - uvicorn 패키지란 웹 서버 구동을 위한 패키지다.
        - Swagger API docs란 FastAPI에서 기본적으로 제공하는 기능으로 어떤 엔드포인트(통신 끝점(컨트롤러 혹은 라우터, api등등))에서 어떤 Input, Output이 예상되는지 확인할 수 있다.
        - Github와 Gitlab의 차이는 초기 설정과 이후에 병합, 분리에 차이가 있다. Github는 ci cd를 위해서 젠킨스같은 프로그램을 따로 사용해야 하지만 Gitlab은 데브 옵스 워크플로우(ci cd)가 이미 내장 되어 있다. 하지만 이후에 병합, 분리에서는 깃허브가 더 빠르며 깃랩에서는 병합, 분리가 느린 대신 코드 안정성이 높다(병합을 위해 여러가지 테스트를 거친다).
        - 아마존 EC2란? [Amazon Elastic Compute Cloud (Amazon EC2)](https://buw.medium.com/aws-ec2%EB%9E%80-%EB%AC%B4%EC%97%87%EC%9D%B4%EB%A9%B0-%EC%99%9C-%EA%B8%B0%EC%97%85%EB%93%A4%EC%9D%B4-ec2%EB%A5%BC-%EC%84%A0%ED%83%9D%ED%95%A0%EA%B9%8C%EC%9A%94-e4c4d6b419b4) 약자로 가상 서버를 다룰 수 있도록 도와주고 사용량만큼 금액을 지불하는 방식의 서비스
        - EC2에서 우분투로 가상머신과 인스턴스를 생성하고 인스턴스에 접속하여 docker, gitlab-runner 프로그램을 설치하고 토큰을 통해 등록할 수 있다.
        - VScode에서 깃랩의 runner를 사용하는 리포지토리인지 아닌지 감지하기 위해서는 .gitlap-ci.yml 파일이 필요하다.
        - 도커로 프로그래밍 언어 이미지를 불러오기 위해선 Dockerfile이 필요하다.
        - 도커에서 환경 설정을 관리 해줄 때 목록 파일을 따로 만들어주기 힘들므로 pip freeze > requirements.txt 명령어로 설치 목록 파일을 생성한다.
        - 위와 같이 dockerfile, requirements.txt 파일을 생성하는 과정 즉, 도커 컨테 컨테이너를 생성하는 과정이 dockerize라고 한다.
        - 웹 서버의 관점에서 ***프록시 서버***는 웹 페이지를 요청, 응답하는 웹 서버(중간다리 역할)
        - cdn이란, Content Delivery Network의 약자인 ***CDN***은 지리적 제약 없이 전 세계 사용자에게 빠르고 안전하게 콘텐츠를 전송할 수 있는 콘텐츠 전송 기술을 의미
  
