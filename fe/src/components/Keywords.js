import { useState } from "react";

import styles from "./Components.module.css";

function Keywords({ answer, setIsCheck, keywords }) {

    const [selected, setSelected] = useState('');

    const onChangeHandler = e => {

        setSelected(e.target.value);
    };

    const onClickHandler = e => {

        if (selected === answer) {

            alert("정답입니다");
        } else {

            alert("오답입니다");
        };

        setSelected('');
        setIsCheck(prev => !prev);
    };

    return (
        <>
            <div className={styles.container}>
                <div className={styles.landscapeBox}>
                    {keywords.length > 0 &&
                        <div style={{ display: "flex", justifyContent: "space-around", alignContent: "center" }}>
                            <div className={styles.keywords}>
                                {keywords.map((word, index) => (
                                    <button
                                        key={index}
                                        value={word}
                                        onClick={onChangeHandler}
                                        style={{ backgroundColor: selected === word ? "aquamarine" : "white" }}
                                    >
                                        {word}
                                    </button>
                                ))}
                            </div>
                            <button
                                className={styles.submitBtn}
                                onClick={onClickHandler}
                                disabled={selected === ''}
                            >
                                확인
                            </button>
                        </div>
                    }
                </div>
            </div>
        </>
    );
};

export default Keywords;