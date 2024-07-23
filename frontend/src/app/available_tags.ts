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

import { Tag, TagsController, Value } from "../model/models";

export class AvailableTags implements TagsController {
    private readonly _tags: Tag[];
    private readonly _tagsMap: Map<
        string,
        {
            value: string;
            values: Map<string, string>;
        }
    >;

    constructor(tags: Tag[]) {
        this._tags = tags;

        this._tagsMap = new Map(
            tags.map((t) => [
                t.key.id,
                {
                    value: t.key.value,
                    values: new Map(t.values.map((v) => [v.id, v.value])),
                },
            ]),
        );
    }

    get tags(): Tag[] {
        return this._tags;
    }

    get keys(): Value[] {
        return Array.from(this._tagsMap, ([k, v]) => ({
            id: k,
            value: v.value,
        }));
    }

    filterValues(keyId: string): Value[] {
        const valuesMap = this._tagsMap.get(keyId)?.values || new Map();
        return Array.from(valuesMap, ([k, v]) => ({ id: k, value: v }));
    }

    getKeyName(keyId: string): string | undefined {
        return this._tagsMap.get(keyId)?.value;
    }

    getValueName(keyId: string, valueId: string): string | undefined {
        return this._tagsMap.get(keyId)?.values.get(valueId);
    }
}
