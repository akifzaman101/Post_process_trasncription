import uuid
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from transcription.services.s3_services import S3Service
from transcription.services.merge_service import MergeService

class UploadChunkView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get("chunk")
        if not file_obj:
            return Response({
                "error": "No file provided. File must be uploaded with 'chunk' key."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        session_id = request.data.get("session_id")
        if not session_id:
            session_id = str(uuid.uuid4())
        
        chunk_index = request.data.get("chunk_index")
        if chunk_index is None:
            return Response({
                "error": "No chunk_index provided."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            chunk_index_int = int(chunk_index)
        except ValueError:
            return Response({
                "error": "chunk_index must be an integer."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        chunk_name = f"{chunk_index_int:06d}"
        
        path = f"recordings/{session_id}/Recording_Chunks/chunk_{chunk_name}.webm"
        
        try:
            S3Service().upload_chunks(file_obj, path)
        except Exception as e:
            return Response({
                "error": "Failed to upload chunk to S3.",
                "details": str(e),
                "chunk_index": chunk_index_int
                
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(
            {
                "message": "Chunk uploaded successfully.",
                "session_id": session_id,
            },
            status=status.HTTP_200_OK
        )
        

class MergeChunksView(APIView):
    
    def post(self, request):
        session_id = request.data.get("session_id")

        if not session_id:
            return Response({"error": "session_id is required"}, status=400)

        try:
            final_path = MergeService().merge_audio_chunks(session_id)
            return Response({
                "message": "Merging completed",
                "merged_file_path": final_path
            })
        except Exception as e:
            return Response({
                "error": "Merging failed",
                "details": str(e)
            }, status=500)
        
