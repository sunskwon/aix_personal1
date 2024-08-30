import { useState } from "react";

import { GetAPI } from "../apis/FastApi";

import styles from "./Components.module.css";

function GenKeyword({ setAnswer, setKeywords, setUrls }) {

    const [sid, setSid] = useState(100);

    const onChangeHandler = e => {

        setSid(e.target.value);
    };

    const onClickHandler = async () => {

        function shuffle(array) {
            array.sort(() => Math.random() - 0.5);
        };

        const res = await GetAPI(`/keyword?sid=${sid}`).then(res => res.json());

        console.log(res);

        let tempArray = res.main_keywords;

        if (tempArray.indexOf(res.sub_keywords[0]) === -1) {

            tempArray.push(res.sub_keywords[0]);
        } else {

            tempArray.push(res.sub_keywords[1]);
        }

        shuffle(tempArray);

        setAnswer(res.sub_keywords[0]);
        setKeywords(tempArray);
        setUrls(res.selected_arts);
    };

    return (
        <>
            <div className={styles.container}>
                <div className={styles.landscapeBox}>
                    <div className={styles.selectBox}>
                        <label htmlFor="sidSelector">분야: </label>
                        <select
                            id="sidSelector"
                            onChange={onChangeHandler}
                            defaultValue={sid}
                        >
                            <option value={100}>정치</option>
                            <option value={101}>경제</option>
                            <option value={102}>사회</option>
                            <option value={103}>생활/문화</option>
                            <option value={104}>세계</option>
                            <option value={105}>IT/과학</option>
                        </select>
                    </div>
                    <button
                        className={styles.submitBtn}
                        onClick={onClickHandler}
                    >
                        키워드 생성
                    </button>
                </div>
            </div>
        </>
    );
};

export default GenKeyword;