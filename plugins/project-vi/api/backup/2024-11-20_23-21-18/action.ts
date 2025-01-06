/* eslint-disable sort-keys-fix/sort-keys-fix, typescript-sort-keys/interface */
// Disable the auto sort key eslint rule to make the code more logic and readable
import { copyToClipboard } from '@lobehub/ui';
import isEqual from 'fast-deep-equal';
import { produce } from 'immer';
import { template } from 'lodash-es';
import { SWRResponse, mutate } from 'swr';
import { StateCreator } from 'zustand/vanilla';

import { LOADING_FLAT } from '@/const/message';
import { TraceEventType, TraceNameMap } from '@/const/trace';
import { useClientDataSWR } from '@/libs/swr';
import { chatService } from '@/services/chat';
import { CreateMessageParams, messageService } from '@/services/message';
import { topicService } from '@/services/topic';
import { traceService } from '@/services/trace';
import { useAgentStore } from '@/store/agent';
import { agentSelectors } from '@/store/agent/selectors';
import { chatHelpers } from '@/store/chat/helpers';
import { messageMapKey } from '@/store/chat/slices/message/utils';
import { ChatStore } from '@/store/chat/store_old';
import { useSessionStore } from '@/store/session';
import { ChatMessage, ChatMessageError, MessageToolCall } from '@/types/message';
import { TraceEventPayloads } from '@/types/trace';
import { setNamespace } from '@/utils/storeDebug';
import { nanoid } from '@/utils/uuid';