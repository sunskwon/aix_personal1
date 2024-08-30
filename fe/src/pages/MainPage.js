import { useEffect, useState } from "react";

import ChatList from "../components/ChatList";
import GenKeyword from "../components/GenKeyword";
import InputQuestion from "../components/InputQuestion";
import Keywords from "../components/Keywords";

import styles from "./Pages.module.css";

function MainPage() {

    const [answer, setAnswer] = useState('');
    const [chatList, setChatList] = useState([]);
    const [isCheck, setIsCheck] = useState(false);
    const [keywords, setKeywords] = useState([]);
    const [urls, setUrls] = useState([]);

    useEffect(() => {

        setAnswer('');
        setChatList([]);
        setKeywords([]);
        setUrls([]);
    }, [isCheck]);

    return (
        <>
            <div className={styles.outerContainer}>
                <GenKeyword
                    setAnswer={setAnswer}
                    setKeywords={setKeywords}
                    setUrls={setUrls}
                />
                <Keywords
                    answer={answer}
                    setIsCheck={setIsCheck}
                    keywords={keywords}
                />
                <ChatList
                    chatList={chatList}
                />
                <InputQuestion
                    chatList={chatList}
                    setChatList={setChatList}
                    urls={urls}
                />
            </div>
        </>
    );
};

export default MainPage;