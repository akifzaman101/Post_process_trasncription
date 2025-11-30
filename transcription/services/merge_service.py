import os
import ffmpeg
from .s3_services import S3Service


class MergeService:
    def __init__(self):
        self.s3 = S3Service()

    def merge_audio_chunks(self, session_id):
        prefix = f"recordings/{session_id}/Recording_Chunks/"
        temp_dir = f"/tmp/{session_id}/"

        os.makedirs(temp_dir, exist_ok=True)

        # 1. Get all chunk file names
        files = self.s3.list_files(prefix)
        if not files:
            raise Exception("No chunks found in S3.")

        # Sort by chunk number because S3 listing is alphabetical
        sorted_files = sorted(files, key=lambda f: f["Key"])

        local_files = []

        # 2. Download all chunks locally
        for f in sorted_files:
            filename = f["Key"].split("/")[-1]
            local_path = os.path.join(temp_dir, filename)
            self.s3.download_file(f["Key"], local_path)
            local_files.append(local_path)

        # 3. Build ffmpeg concat file list
        concat_path = os.path.join(temp_dir, "concat.txt")
        with open(concat_path, "w") as f:
            for file in local_files:
                f.write(f"file '{file}'\n")

        # 4. Merge using ffmpeg
        output_file = os.path.join(temp_dir, f"{session_id}_merged.webm")

        (
            ffmpeg
            .input(concat_path, format="concat", safe=0)
            .output(output_file, c="copy")
            .run()
        )

        # 5. Upload merged file back to S3
        final_s3_path = f"recordings/{session_id}/final_audio/{session_id}.webm"
        self.s3.upload_file(output_file, final_s3_path)

        return final_s3_path
