import { useState } from "react";

import { PostAPI } from "../apis/FastApi";

import styles from "./Components.module.css";

function InputQuestion({ chatList, setChatList, urls }) {

    const [query, setQuery] = useState('');

    const onChangeHandler = e => {

        setQuery(e.target.value);
    };

    const onSubmitHandler = async e => {

        e.preventDefault();

        if (chatList.length > 4) {

            alert("더이상 질문할 수 없습니다")
        } else {

            const res = await PostAPI(`/ask?query=${query}`, urls).then(res => res.json());

            console.log(res.answer);

            setChatList(prevChatList => [
                ...prevChatList,
                {
                    'question': query,
                    'answer': res.answer
                }
            ]);
        };

        setQuery('');
    };

    return (
        <>
            <div className={styles.container}>
                <div className={styles.landscapeBox}>
                    <form
                        className={styles.formBox}
                        onSubmit={onSubmitHandler}
                    >
                        <input
                            type="text"
                            value={query}
                            onChange={onChangeHandler}
                        />
                        <button className={styles.submitBtn}>전송</button>
                    </form>
                </div>
            </div>
        </>
    );
};

export default InputQuestion;