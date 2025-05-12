import React, { useState, useRef } from 'react';

import CloseIcon from '../../../../assets/close.svg';
import FileIcon from '../../../../assets/file.svg';

type SelectFileComponentProps = {
    onFileSelect: (file: File) => void;
};

const SelectFileComponent: React.FC<SelectFileComponentProps> = ({ onFileSelect }) => {
    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const inputFileRef = useRef<HTMLInputElement>(null);

    const [PDFError, setPDFError] = useState<boolean>(false);

    const triggerFileSelect = () => inputFileRef.current?.click();

    const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            setSelectedFile(event.target.files[0]);
        }
    };

    const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
    };

    const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
            const file = event.dataTransfer.files[0];
            if (file.type === "application/pdf") {
                setSelectedFile(file);
                event.dataTransfer.clearData();
            } else {
                setPDFError(true)
            }
        }
    };

    const handleUploadClick = () => {
        if (selectedFile) {
            onFileSelect(selectedFile);
            setSelectedFile(null); // Optionally reset the selected file after triggering the upload
        }
    };

    return (
        <div>

            <div className='flex flex-col justify-center content-center'>

                <div
                    onClick={triggerFileSelect}
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                    className="cursor-pointer border-2 rounded border-indigo-200 p-5 w-full text-center flex flex-col justify-center items-center h-48
                            hover:border-indigo-400 hover:shadow-md"
                >

                    {!selectedFile ? (
                        <div>
                            <p>Select or drag a PDF file here</p>
                        </div>
                    ) : (
                        <div className='flex justify-center items-center h-20 text-center border-2 px-4 border-indigo-200 rounded-lg'>
                            <img src={FileIcon} alt='icon file' className="w-8 h-8 mr-3" />
                            <p className='mr-4'>{selectedFile.name}</p>

                            <button
                                className='bg-indigo-200 rounded-full p-2 mx-2 flex items-center justify-center'
                                onClick={(event) => {
                                    event.stopPropagation();
                                    setSelectedFile(null)
                                    if (inputFileRef.current) {
                                        inputFileRef.current.value = "";
                                    }
                                }}
                            >
                                <img src={CloseIcon} alt='Close' className="w-6 h-6" />
                            </button>

                        </div>
                    )}

                    <input
                        type="file"
                        onChange={handleChange}
                        className="hidden"
                        ref={inputFileRef}
                        accept=".pdf"
                    />
                    
                </div>

                {!selectedFile ? (
                    <button
                        onClick={triggerFileSelect}
                        className="mt-4 bg-indigo-500 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded"
                    >
                        Choose File
                    </button>
                ) : (
                    <button
                        onClick={handleUploadClick}
                        className="mt-4 bg-violet-500 hover:bg-violet-700 text-white font-bold py-2 px-4 rounded"
                    >
                        Start Upload
                    </button>
                )}

            </div>
            
            <div className='flex justify-center items-center'>
                {PDFError && (
                    <div className='flex justify-center items-center h-16 w-fit text-center border-2 px-4 border-red-700 bg-red-200 rounded-lg mt-6'>
                        <p className='mx-4'>Only PDF files are accepted</p>
                        <button
                            className='bg-red-500 rounded-full p-2 flex items-center justify-center'
                            onClick={(event) => {
                                event.stopPropagation();
                                setPDFError(false)
                            }}
                        >
                            <img src={CloseIcon} alt='Close' className="w-6 h-6" />
                        </button>
                        
                    </div>
                )}
            </div>



        </div>

    );
};

export default SelectFileComponent;
