/*
   Copyright 2024 Google LLC

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       https://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
*/

export type Value = {
    id: string;
    value: string;
};

export type TagBinding = {
    id: string;
    value: string;
};

export type Resource = {
    id: string;
    name: string;
    type: string;
    location: string;
    tags: TagBinding[];
};

export type Tag = {
    key: Value;
    values: Value[];
};

export type Response = {
    message: string;
};

export type BulkResponse = {
    message: string;
    errors: string[];
};

export interface TagsController {
    get tags(): Array<Tag>;
    get keys(): Array<Value>;

    filterValues(keyId: string): Array<Value>;
    getKeyName(keyId: string): string | undefined;
    getValueName(keyId: string, valueId: string): string | undefined;
}
