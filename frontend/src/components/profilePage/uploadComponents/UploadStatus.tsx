import React from 'react';

type UploadStatusComponentProps = {
    progress: number | null; // Accepts null for indeterminate progress
    status: 'uploading' | 'done';
};

const UploadStatusComponent: React.FC<UploadStatusComponentProps> = ({ progress, status }) => {
    if (status === 'uploading') {
        return (
            <div>
                {progress !== null ? (
                    <p>Uploading... {progress}%</p>
                ) : (
                    <p>Uploading... (size unknown)</p>
                )}
            </div>
        );
    } else if (status === 'done') {
        return <p>Upload completed!</p>;
    }

    return null; // Should never reach here
};


export default UploadStatusComponent;