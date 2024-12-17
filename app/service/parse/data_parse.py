def parse_scrap_data(soup, recipe_id):
    recipe_data = {}
    
    # 레시피 제목 추출
    title_div = soup.find('div', class_='view2_summary')
    if title_div:
        title = title_div.find('h3').get_text(strip=True)
        recipe_data['title'] = title
    else:
        return {"error": f"ID {recipe_id}에 대한 레시피 제목을 찾을 수 없습니다."}
    
    # 재료 추출
    ingredients = {}
    ingredient_div = soup.find('div', class_='ready_ingre3')
    if ingredient_div:
        for ul in ingredient_div.find_all('ul'):
            b_tag = ul.find('b', class_='ready_ingre3_tt')
            category = b_tag.get_text(strip=True) if b_tag else "재료"
            items = []
            for li in ul.find_all('li'):
                name_tag = li.find('div', class_='ingre_list_name')
                amount_tag = li.find('span', class_='ingre_list_ea')
                name = name_tag.get_text(strip=True) if name_tag else ""
                amount = amount_tag.get_text(strip=True) if amount_tag else ""
                if name:
                    items.append(f"{name} {amount}".strip())
            ingredients[category] = items
        recipe_data['ingredients'] = ingredients
    else:
        return {"error": f"ID {recipe_id}에 대한 재료 정보를 찾을 수 없습니다."}
    
    # 조리 단계 추출
    steps = []
    step_div = soup.find('div', class_='view_step')
    if step_div:
        for i, step in enumerate(step_div.find_all('div', class_='view_step_cont'), 1):
            steps.append(f"Step {i}: {step.get_text(strip=True)}")
        recipe_data['steps'] = steps
    else:
        return {"error": f"ID {recipe_id}에 대한 조리 단계를 찾을 수 없습니다."}
    
    return recipe_data
    
    return recipe_data

def parse_scrap_id(soup):
    # 레시피 링크를 선택
    recipe_links = soup.select('a.common_sp_link')
    # 각 링크에서 레시피 ID 추출
    recipe_ids = [link['href'].split('/')[-1] for link in recipe_links]
    return recipe_ids
