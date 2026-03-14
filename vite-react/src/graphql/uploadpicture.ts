import { gql } from '@apollo/client';

export const UPLOAD_PICTURE = gql`
  mutation UploadPicture($input: UploadInput!) {
    upload_picture(input: $input) {
        message
        userpic
    }
  }
`;

export interface UserData {
  id: number;
  firstname: string;
  lastname: string;
  email: string;
  mobile: string;
  username: string;
  isactivated: boolean;
  isblocked: boolean;
  mailtoken: string;
  userpic: string;
  qrcodeurl: string;
}

export interface UploadData {
  user: UserData;
}

export interface UploadVariables {
  id: number;
  file: File;
}
