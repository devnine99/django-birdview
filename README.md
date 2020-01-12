# 화해(버드뷰) 프로그래머스 챌린지 Django 프로젝트

## Project 요약
- 장고(3.0.1)의 DRF를 활용한 REST API 구축
- RDBMS 사용 
- local 환경에서 sqlite3 사용
- staging, production 환경에서 postgresql 사용
- aws ec2에 배포(ubuntu 18.04LTS)
- nginx, gunicorn으로 웹서버 및 웹앱서버 구성


### Product(상품)
- Product(상품)와 Ingredient(구성성분) 모델
- Product N:N Ingredient 관계
- 상품리스트  
-- 고객의 피부 타입에 따라 상품의 구성성분을 분석하여 점수를 매겨 점수가 높은 순으로 보여줌, 이를 구현하기 위해 ProductManager 작성  
-- 고객이 요청한 카테고리, 포함성분, 불포함성분을 필터링하여 보여줌  
-- 한 페이지에 50개씩 페이지네이션
- 상품상세  
-- 고객이 요청한 상품을 보여주고, 고객의 피부 타입에 따라 추천 상품 3개를 보여줌
