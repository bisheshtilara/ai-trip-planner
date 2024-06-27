import { Icon } from "@iconify/react";
import React from "react";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import Recorder from "./components/Recorder";
import { Language } from "./type";

const languageTabs = [
  {
    language: "English",
    tab: "En",
    code: Language.EN,
  },
  {
    language: "French",
    tab: "Fr",
    code: Language.FR,
  },
];

const App: React.FC = () => {
  const [language, setLanguage] = React.useState<Language | null>(null);

  // error
  const [error, setError] = React.useState<string>("");

  if (!language)
    return (
      <div className="bg-gray-100 min-h-screen flex gap-10 justify-center items-center overflow-auto">
        {languageTabs.map((tab, index) => (
          <div
            key={index}
            className="grid justify-items-center gap-y-2"
            onClick={() => setLanguage(tab.code)}
          >
            <div
              className="text-red-500 flex justify-center items-center p-5 rounded-lg shadow-md hover:scale-105 duration-300 w-32 border-t text-7xl"
              role="button"
            >
              {tab.tab}
            </div>
            <small className="font-extralight">{tab.language}</small>
          </div>
        ))}
      </div>
    );

  return (
    <div className="bg-gray-100 h-screen relative p-5">
      <button
        className="top-16 left-16 absolute transition-all ease-in-out hover:scale-110 duration-300"
        onClick={() => setLanguage(null)}
      >
        <Icon icon="bi:chevron-left" width="1rem" />
      </button>
      <div className="py-16 space-y-8">
        <Recorder
          {...{
            language,
            setError,
            error,
          }}
        />
        {error && (
          <p className="text-red-500 text-center text-sm underline">
            Error: {error}
          </p>
        )}
      </div>
      <ToastContainer />
    </div>
  );
};

export default App;
