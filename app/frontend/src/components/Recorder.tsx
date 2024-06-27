import { Icon } from "@iconify/react";
import axios from "axios";
import React from "react";
import { CircleLoader } from "react-spinners";
import { Language, NLP } from "../type";

interface TravelOptimizer {
  origin: string;
  destination: string;
}

interface Itinerary {
  start_station: string;
  end_station: string;
}

interface PathFinder {
  optimized_shortest_path: string[];
  itinerary: Itinerary[];
  travel_optimization_details: {
    start_station: string;
    end_station: string;
    route_id: string;
  }[];
}

const AudioRecorder: React.FC<{
  language: Language;
  error: string;
  setError: React.Dispatch<React.SetStateAction<string>>;
}> = ({ language, error, setError }) => {
  const [audioData, setAudioData] = React.useState<string | null>(null);
  const mediaRecorderRef = React.useRef<MediaRecorder | null>(null);
  const [isRecording, setIsRecording] = React.useState(false);
  const [isGettingNlp, setIsGettingNlp] = React.useState(false);
  const [nlp, setNlp] = React.useState<NLP | undefined>();
  const [input, setInput] = React.useState<string | undefined>();
  const [textInput, setTextInput] = React.useState<string>("");
  const [pathfinder, setPathfinder] = React.useState<PathFinder | undefined>();

  React.useEffect(() => {
    console.log(pathfinder);
  }, [pathfinder]);

  React.useEffect(() => {
    if (!audioData) return;
    getNlp("voice");

    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [audioData]);

  const startRecording = async () => {
    setIsRecording(true);
    setError("");
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);

      const chunks: Blob[] = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunks.push(e.data);
        }
      };

      mediaRecorder.onstop = () => {
        const blob = new Blob(chunks, { type: "audio/wav" });

        // Convert audio data to base64 and set it in the state
        const reader = new FileReader();
        reader.onloadend = () => {
          const base64Data = (reader.result as string).split(",")[1];
          setAudioData(base64Data);
        };
        reader.readAsDataURL(blob);
      };

      mediaRecorderRef.current = mediaRecorder;
      mediaRecorder.start();
    } catch (error) {
      setError("Error accessing microphone");
      console.error("Error accessing microphone:", error);
    }
  };

  const stopRecording = async () => {
    setIsRecording(false);
    if (mediaRecorderRef.current) {
      mediaRecorderRef.current.stop();
    }
  };

  const getNlp = async (type: string) => {
    let catchnlp = {
      origin: null,
      destination: null,
    };
    setError("");
    try {
      setIsGettingNlp(true);
      const res = await axios.post(
        `http://localhost:8000/${type}`,
        type === "voice"
          ? {
              file_content: audioData,
              language_code: language,
            }
          : {
              text: textInput,
              language_code: language,
            },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (type === "voice") setInput(res.data.input_voice);

      setIsGettingNlp(false);

      catchnlp = res.data.nlp;

      if (
        res.status !== 200 ||
        Object.values(res.data.nlp).some((value) => value === null)
      )
        throw new Error("NLP request failed");

      setNlp(res.data.nlp);

      if (res.data.nlp) await getPathFinder(res.data.nlp);
      else setPathfinder(undefined);
    } catch (error) {
      if (catchnlp.origin === null && catchnlp.destination === null)
        setError("Invalid origin and destination");
      else if (catchnlp.origin === null) setError("Invalid origin");
      else if (catchnlp.destination === null) setError("Invalid destination");
      setError("Please make sure that the origin and destination are valid");
    }
  };

  const getPathFinder = async (travelOptimizer: TravelOptimizer) => {
    setError("");
    try {
      const res = await axios.post(
        "http://localhost:8000/path-finder",
        {
          origin: travelOptimizer.origin,
          destination: travelOptimizer.destination,
        },
        {
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      if (
        res.status !== 200 ||
        !res.data ||
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        Object.values(res.data.data).some((value: any) => value.length === 0)
      )
        throw new Error("Path Finder request failed");
      else setPathfinder(res.data.data);
    } catch (error) {
      setError(
        "Pathfinder request failed! Please make sure that the origin and destination are valid"
      );
    }
  };

  const handleTextInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const value = e.target.value;
    setTextInput(value);
    setInput(value);
  };

  return (
    <div className="grid justify-items-center gap-y-8">
      <Input
        {...{
          startRecording,
          stopRecording,
          isGettingNlp,
          isRecording,
          handleTextInputChange,
          getNlp,
          language,
          input,
          textInput,
        }}
      />
      {isGettingNlp && <CircleLoader color="red" size={100} />}
      {!error &&
        !isGettingNlp &&
        nlp &&
        !Object.values(nlp).some((value) => value === null) && (
          <div className="flex gap-x-4 justify-between max-w-sm w-full">
            {[
              { station: nlp.origin, label: "Origin" },
              { station: nlp.destination, label: "Destination" },
            ].map(({ station, label }, index) => (
              <div
                key={index}
                className="flex gap-4 bg-red-500 rounded px-2 py-0.5 shadow border border-white ring-2 ring-red-500"
              >
                <h2 className="text-xs text-white font-light">{`${label}:  ${station}`}</h2>
              </div>
            ))}
          </div>
        )}
      {!error && !isGettingNlp && pathfinder && (
        <div className="flex max-w-xl w-full justify-center mt-10">
          <div className="space-y-4 h-full max-h-[28rem] overflow-y-scroll border-t shadow-md p-5 rounded-xl w-full max-w-sm">
            {pathfinder.travel_optimization_details.map(
              ({ start_station, end_station }, index) => (
                <div
                  key={index}
                  className="grid grid-cols-3 items-center px-4 py-3 shadow rounded-md border-t"
                >
                  <p className="justify-self-start text-sm">{start_station}</p>
                  <Icon
                    icon="bi:arrow-right"
                    color="black"
                    className="justify-self-center"
                  />
                  <p className="justify-self-end text-sm">{end_station}</p>
                </div>
              )
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AudioRecorder;

const Input: React.FC<{
  startRecording: () => Promise<void>;
  stopRecording: () => Promise<void>;
  isRecording: boolean;
  handleTextInputChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
  getNlp: (type: string) => Promise<void>;
  language: Language;
  input: string | undefined;
  textInput: string;
}> = ({
  startRecording,
  stopRecording,
  isRecording,
  handleTextInputChange,
  getNlp,
  language,
  input,
  textInput,
}) => {
  return (
    <div className="max-w-3xl w-full flex items-center gap-x-4 justify-center">
      <button
        className="rounded-xl bg-red-500 py-3 px-3.5 hover:-translate-x-2 duration-300 transition-all"
        onMouseDown={startRecording}
        onMouseUp={stopRecording}
      >
        {isRecording ? (
          <CircleLoader color="#fff" size={24} />
        ) : (
          <Icon icon="lucide:mic" width="1.5rem" color="white" />
        )}
      </button>
      <div className="flex items-center gap-x-4 w-3/4 rounded-xl">
        <input
          type="text"
          className="p-4 focus:outline-none w-full rounded-md shadow text-sm placeholder:opacity-50"
          onChange={handleTextInputChange}
          placeholder={
            language === Language.EN
              ? "I want to go from Paris to Montpellier"
              : "Je veux aller de Paris à Montpellier"
          }
          value={input || textInput}
        />
        <button
          className="rounded-xl bg-red-500 p-3 hover:translate-x-2 duration-300 transition-all"
          onClick={() => getNlp("input")}
        >
          <Icon icon="bi:chevron-right" width="1.5rem" color="white" />
        </button>
      </div>
    </div>
  );
};
