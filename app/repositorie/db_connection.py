from app.core import setting
from pinecone import Pinecone, ServerlessSpec
import re
from typing import List,Dict

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DatabaseConnection:
    _instance = None
    _index = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            # Pinecone 인스턴스 생성
            pc = Pinecone(api_key=setting.PINECONE_API_KEY)

            index_name = "recipes"
            dimension = 1024

            # 인덱스 존재 여부 확인
            if index_name not in pc.list_indexes().names():
                pc.create_index(
                    name=index_name,
                    dimension=dimension,
                    metric='cosine',
                    spec=ServerlessSpec(
                        cloud='aws',
                        region='us-east-1'
                    )
                )
                logger.info(f"인덱스 '{index_name}'가 생성되었습니다.")
            else:
                logger.info(f"인덱스 '{index_name}'는 이미 존재합니다. 기존 인덱스를 사용합니다.")

            # 인덱스 불러오기
            cls._index = pc.Index(index_name)
        return cls._instance

    def __init__(self):
        self.index = self._index

    async def upsert_recipe(self, recipe_id, embedding, metadata):
        # ID로 기존 데이터 검색
        existing_data = self.index.fetch(ids=[str(recipe_id)])
        
        if existing_data.vectors:
            # 기존 데이터가 있으면 업데이트
            logger.info(f"레시피 {recipe_id} 업데이트 중...")
            self.index.update(
                id=str(recipe_id),
                values=embedding,
                metadata=metadata
            )
            return {"status": "updated"}
        else:
            # 새로운 데이터 삽입
            logger.info(f"새로운 레시피 {recipe_id} 추가 중...")
            self.index.upsert(vectors=[{
                'id': str(recipe_id),
                'values': embedding,
                'metadata': metadata
            }])
            return {"status": "inserted"}

    # 재료 이름에서 양과 단위를 제거하는 함수
    def strip_quantities(self, ingredients: List[str]) -> List[str]:
        cleaned_ingredients = []
        for ingredient in ingredients:
            # 숫자와 단위 제거를 위한 더 포괄적인 패턴
            ingredient = re.sub(r'\d+\.?\d*[a-zA-Z가-힣]*', '', ingredient)
            # 분수 형태 제거
            ingredient = re.sub(r'\d+\/\d+', '', ingredient)
            # 측정 단위 제거
            ingredient = re.sub(r'(약간|T|t|컵|큰술|작은술|숟가락|스푼|g|kg|ml|L)', '', ingredient)
            # 남은 숫자들 제거
            ingredient = re.sub(r'\d+', '', ingredient)
            # 특수문자 제거 (슬래시, 물결표 등)
            ingredient = re.sub(r'[/~]+', '', ingredient)
            # 양쪽 공백 제거하고 결과 추가
            cleaned = ingredient.strip()
            if cleaned:  # 빈 문자열이 아닌 경우만 추가
                cleaned_ingredients.append(cleaned)
        return cleaned_ingredients
    
    def extract_ingredient_name(self, ingredient:str) -> str:
        # 괄호와 슬래시, 물결표 등 불필요한 문자 제거
        return re.match(r'([^(/~]+)', ingredient).group(1).strip()
    
    def process_ingredients(self, recipe_metadata: Dict) -> List[str]: #메타데이터에서 재료만 추출
        return [self.extract_ingredient_name(ing) for ing in recipe_metadata['ingredients']]