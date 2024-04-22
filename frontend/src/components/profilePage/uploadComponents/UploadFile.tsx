import React, { useEffect } from 'react';

import axios from 'axios';
import { getUsernameBySession } from '../../../utils/utils';

type UploadFileComponentProps = {
    file: File;
    onUploadProgress: (percentage: number | null) => void; // Updated to allow null
    onUploadComplete: () => void;
    onError: (error: any) => void;
};

const UploadFileComponent: React.FC<UploadFileComponentProps> = ({
    file,
    onUploadProgress,
    onUploadComplete,
    onError,
}) => {
    useEffect(() => {
        const uploadFile = async () => {
            const formData = new FormData();
            formData.append('file', file);

            const username = await getUsernameBySession()

            try {
                await axios.post(`http://localhost:3003/upload/${username}`, formData, {
                    onUploadProgress: (progressEvent) => {
                        if (progressEvent.total) {
                            const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                            onUploadProgress(percentCompleted);
                        } else {
                            // Handle case where total size is unknown
                            onUploadProgress(null);
                        }
                    }
                });
                onUploadComplete();
            } catch (error) {
                onError(error);
            }

        };

        if (file) {
            uploadFile();
        }
    }, [file, onUploadComplete, onError, onUploadProgress]);

    return <div>Uploading {file.name}</div>;
};


export default UploadFileComponent;