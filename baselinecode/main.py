import os
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from config import ExperimentConfig
from prompts.templates import TEMPLATES
from utils.experiment import ExperimentRunner


def main():
    # API 키 로드
    load_dotenv()
    api_key = os.getenv('UPSTAGE_API_KEY')
    if not api_key:
        raise ValueError("API key not found in environment variables")
    
    # 기본 설정 생성
    base_config = ExperimentConfig(template_name='sth_version5')
    
    # 데이터 로드
    train = pd.read_csv(os.path.join(base_config.data_dir, 'train.csv'))
    test = pd.read_csv(os.path.join(base_config.data_dir, 'test.csv'))
    
    # 토이 데이터셋 생성
    toy_data = train.sample(n=base_config.toy_size, random_state=base_config.random_seed).reset_index(drop=True)
    
    # train/valid 분할
    train_data, valid_data = train_test_split(
        toy_data,
        test_size=base_config.test_size,
        random_state=base_config.random_seed
    )
    
    # 모든 템플릿으로 실험
    results = {}
    for template_name in TEMPLATES.keys():
        config = ExperimentConfig(
            template_name=template_name,
            temperature=0.0,
            batch_size=5,
            experiment_name=f"toy_experiment_{template_name}"
        )
        runner = ExperimentRunner(config, api_key)
        results[template_name] = runner.run_template_experiment(train_data, valid_data)

    # 결과 비교
    print("\n=== 템플릿별 성능 비교 ===")
    for template_name, result in results.items():
        print(f"\n[{template_name} 템플릿]")
        print("Train Recall:", f"{result['train_recall']['recall']:.2f}%")
        print("Train Precision:", f"{result['train_recall']['precision']:.2f}%")
        print("\nValid Recall:", f"{result['valid_recall']['recall']:.2f}%")
        print("Valid Precision:", f"{result['valid_recall']['precision']:.2f}%")
        
        output_dir = "data"
        # 학습 결과에 "source" 컬럼 추가
        train_df = result["train_results"].copy()
        train_df["source"] = "train"

        # 검증 결과에 "source" 컬럼 추가
        valid_df = result["valid_results"].copy()
        valid_df["source"] = "valid"

        # 두 개 DataFrame 병합
        merged_df = pd.concat([train_df, valid_df], ignore_index=True)
        merged_df = merged_df[["id", "source", "err_sentence", "cor_sentence"]]  # 컬럼 정리

        # 저장
        save_path = os.path.join(output_dir, f"merged_train_valid_{template_name}.csv")
        merged_df.to_csv(save_path, index=False)
        
        print(f"[{template_name}] 병합된 결과 저장 완료 ✅")
    
    # 최고 성능 템플릿 찾기
    best_template = max(
        results.items(), 
        key=lambda x: x[1]['valid_recall']['recall']
    )[0]
    

    print(f"\n최고 성능 템플릿: {best_template}")
    print(f"Valid Recall: {results[best_template]['valid_recall']['recall']:.2f}%")
    print(f"Valid Precision: {results[best_template]['valid_recall']['precision']:.2f}%")
    print(results)
    



    # 두번째 과정 진행 데이터셋 구축
    # 1차 결과에서 가져오기
    # results_df = results[best_template]["train_results"].copy()

    # # 1차 교정 결과 보존
    # results_df.rename(columns={"cor_sentence": "cor_sentence_1"}, inplace=True)

    # # 원래 정답과 병합 (비교용 정답: train["cor_sentence"])
    # results_df = results_df.merge(train[["id", "cor_sentence"]], on="id", how="left")

    # # 2차 교정 입력값 설정 (1차 결과 → 2차 입력)
    # results_df["err_sentence"] = results_df["cor_sentence_1"]

    # # 컬럼 구조 확인
    # print(results_df.columns)
    # # ['id', 'err_sentence', 'cor_sentence_1', 'cor_sentence']

    # print(results_df.info())
    # results_df.to_csv("/Users/seojeonghun/Desktop/비타민/데이터톤/project/data/first_v1.csv", index=False)

    # # 모든 템플릿으로 실험
    # results_2 = {}
    # for template_name in TEMPLATES_2.keys():
    #     config = ExperimentConfig_2(
    #         template_name=template_name,
    #         temperature=0.0,
    #         batch_size=5,
    #         experiment_name=f"toy_experiment_{template_name}"
    #     )
    #     runner = ExperimentRunner_2(config, api_key)
    #     results_2[template_name] = runner.run_template_experiment(train_data, valid_data)
    # print(results_2)

    # # 결과 비교
    # print("\n=== 템플릿별 성능 비교 ===")
    # for template_name, result in results_2.items():
    #     print(f"\n[{template_name} 템플릿]")
    #     print("Train Recall:", f"{result['train_recall']['recall']:.2f}%")
    #     print("Train Precision:", f"{result['train_recall']['precision']:.2f}%")
    #     print("\nValid Recall:", f"{result['valid_recall']['recall']:.2f}%")
    #     print("Valid Precision:", f"{result['valid_recall']['precision']:.2f}%")
    
    # # 최고 성능 템플릿 찾기
    # best_template = max(
    #     results_2.items(), 
    #     key=lambda x: x[1]['valid_recall']['recall']
    # )[0]

    # print(f"\n최고 성능 템플릿: {best_template}")
    # print(f"Valid Recall: {results_2[best_template]['valid_recall']['recall']:.2f}%")
    # print(f"Valid Precision: {results_2[best_template]['valid_recall']['precision']:.2f}%")
    # print(results_2)

    # # 두번째 과정 진행 데이터셋 구축
    # result_2_df = results_2[best_template]["train_results"].copy()
    # result_2_df.to_csv("/Users/seojeonghun/Desktop/비타민/데이터톤/project/data/second_v1.csv")

    #최고 성능 템플릿으로 제출 파일 생성
    print("\n=== 테스트 데이터 예측 시작 ===")
    config = ExperimentConfig(
        template_name=best_template,
        temperature=0.0,
        batch_size=5,
        experiment_name="final_submission"
    )
    
    runner = ExperimentRunner(config, api_key)
    test_results = runner.run(test)
    
    output = pd.DataFrame({
        'id': test['id'],
        'cor_sentence': test_results['cor_sentence']
    })
    
    output.to_csv("submission_baseline.csv", index=False)
    print("\n제출 파일이 생성되었습니다: submission_baseline.csv")
    print(f"사용된 템플릿: {best_template}")
    print(f"예측된 샘플 수: {len(output)}")

if __name__ == "__main__":
    main()