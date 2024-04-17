import React, { ChangeEvent, DragEvent, useRef, useState } from 'react';
import axios from 'axios';

const UploadSection: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const inputFileRef = useRef<HTMLInputElement>(null);

    const onFileChange = (event: ChangeEvent<HTMLInputElement>) => {
        if (event.target.files && event.target.files[0]) {
            setFile(event.target.files[0]);
        }
    };

    const onDragOver = (event: DragEvent<HTMLDivElement>) => {
        event.preventDefault(); // Prevent default behavior (Prevent file from being opened)
    };

    const onDrop = (event: DragEvent<HTMLDivElement>) => {
        event.preventDefault();
        if (event.dataTransfer.files && event.dataTransfer.files.length > 0) {
            setFile(event.dataTransfer.files[0]);
            event.dataTransfer.clearData();
        }
    };

    const triggerFileSelect = () => {
        inputFileRef.current?.click(); // Trigger the file selection dialog
    };

    return (
        <div
            className="cursor-pointer border-2 border-dashed border-gray-300 p-5 w-72 text-center flex flex-col justify-center items-center h-48"
            onClick={triggerFileSelect}
            onDragOver={onDragOver}
            onDrop={onDrop}
        >
            <p>Drag and drop a file here or click to select a file</p>
            <input
                type="file"
                onChange={onFileChange}
                className="hidden"
                ref={inputFileRef}
            />
            {file && (
                <div className="mt-2 text-sm text-gray-600">
                    File selected: {file.name}
                </div>
            )}
        </div>
    );
};

export default UploadSection;
