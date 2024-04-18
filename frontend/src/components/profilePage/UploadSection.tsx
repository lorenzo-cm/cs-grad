import React, { useState,} from 'react';

import SelectFileComponent from './uploadComponents/SelectFile';
import UploadFileComponent from './uploadComponents/UploadFile';
import UploadStatusComponent from './uploadComponents/UploadStatus';

const UploadSection: React.FC = () => {
    const [file, setFile] = useState<File | null>(null);
    const [progress, setProgress] = useState<number | null>(0);
    const [uploadStatus, setUploadStatus] = useState<'select' | 'uploading' | 'done'>('select');

    const handleFileSelect = (selectedFile: File) => {
        setFile(selectedFile);
        setUploadStatus('uploading');
    };

    const handleUploadProgress = (percentage: number | null) => {
        if (percentage !== null) {
            setProgress(percentage);
        } else {
            // Handle indeterminate progress, e.g., show a spinner or a special message
            setProgress(null);
        }
    };

    const handleUploadComplete = () => {
        setUploadStatus('done');
    };

    const handleError = (error: any) => {
        console.error('Upload error:', error);
        // Handle error visually if needed
    };

    return (
        <div className='mt-8'>
            {uploadStatus === 'select' && <SelectFileComponent onFileSelect={handleFileSelect} />}
            {uploadStatus === 'uploading' && file && (
                <UploadFileComponent
                    file={file}
                    onUploadProgress={handleUploadProgress}
                    onUploadComplete={handleUploadComplete}
                    onError={handleError}
                />
            )}
            {uploadStatus !== 'select' && (
                <UploadStatusComponent progress={progress} status={uploadStatus} />
            )}
        </div>
    );
};

export default UploadSection;